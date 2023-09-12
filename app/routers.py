from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.schemas import PessoaSchema
from app.models import Person
from app.database import get_db
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app import settings
import json

router = APIRouter()
global_settings = settings.get_settings()


@router.get("/ready")
async def ready(db_session: Session = Depends(get_db)):
    table_exists = await Person.table_exists(db_session)
    return {"ready": table_exists}


@router.get(
    "/pessoas", status_code=status.HTTP_200_OK, response_model=List[PessoaSchema]
)
async def search_persons_by_term(t: str, db_session: Session = Depends(get_db)):
    if not t:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid search term.",
        )
    instances = await Person.search_by_term(db_session=db_session, search_term=t)
    return instances


@router.post("/pessoas", status_code=status.HTTP_201_CREATED)
async def create_person(
    request: Request, payload: PessoaSchema, db_session: Session = Depends(get_db)
):
    if payload.nome is None or payload.apelido is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Pessoa nome or apelido can't be null or empty.",
        )

    check_redis = await request.app.state.redis.get(f"nick_{payload.apelido}")
    if check_redis:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Nick taken by other person.",
            # detail={"Not found": f"There is no record for apelido: {apelido}"},
        )
    else:
        # await Person.nick_already_exists(db_session=db_session, nick=payload.apelido)
        await request.app.state.redis.set(
            f"nick_{payload.apelido}",
            str(payload.apelido),
            ex=global_settings.redis_default_expiration,
        )

    person = Person(
        nome=payload.nome,
        apelido=payload.apelido,
        nascimento=payload.nascimento,
        stack=payload.stack,
    )

    person = await person.save(db_session)
    await request.app.state.redis.set(
        f"person_{person.id}",
        json.dumps(person.as_dict()),
        ex=global_settings.redis_default_expiration,
    )

    headers = {"Location": "http://nginx:9999/pessoas/{id}".format(id=person.id)}
    return JSONResponse(
        content=jsonable_encoder(person),
        status_code=status.HTTP_201_CREATED,
        headers=headers,
    )


@router.get(
    "/pessoas/{id}", status_code=status.HTTP_200_OK, response_model=PessoaSchema
)
async def get_person_by_id(
    request: Request, id: int, db_session: Session = Depends(get_db)
):
    person_redis = await request.app.state.redis.get(f"person_{id}")
    if person_redis:
        person = json.loads(person_redis)
        return person
    return await Person.find_by_id(db_session, person_id=id)


@router.put(
    "/pessoas/{id}", status_code=status.HTTP_200_OK, response_model=PessoaSchema
)
async def update_person_by_id(
    payload: PessoaSchema,
    id: int,
    db_session: Session = Depends(get_db),
):
    person = await Person.find_by_id(db_session, person_id=id)
    await person.update(db_session, **payload.model_dump())
    return person


@router.delete("/pessoas/{id}", status_code=status.HTTP_200_OK, response_model=None)
async def delete_person_by_id(id: int, db_session: Session = Depends(get_db)):
    person = await Person.find_by_id(db_session, person_id=id)
    was_deleted = await person.delete(db_session)
    return {"deleted": was_deleted, "message": "Person deleted!"}


@router.get("/contagem-pessoas", status_code=status.HTTP_200_OK, response_model=int)
async def count_persons(db_session: Session = Depends(get_db)):
    return await Person.count(db_session=db_session)
