from fastapi import APIRouter, Request, HTTPException, status, Depends
from typing import Any, List
from sqlalchemy.orm import Session
from app.schemas import PessoaSchema
from app.config import SessionLocal
from app.data import (
    get_pessoa_by_id,
    count_pessoas,
    create_pessoa,
    remove_pessoa,
    search_pessoas,
    update_pessoa,
    get_pessoa_by_apelido,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/pessoas", status_code=status.HTTP_200_OK, response_model=List[PessoaSchema]
)
async def search_by_term(t: str, db: Session = Depends(get_db)):
    if not t:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid search term.",
        )
    instances = search_pessoas(db=db, search_term=t)
    return instances


@router.post("/pessoas")
async def create(request: Request, pessoa: PessoaSchema, db: Session = Depends(get_db)):
    instance_exist = get_pessoa_by_apelido(db=db, pessoa=pessoa)
    if instance_exist:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Pessoa already exists.",
        )

    if pessoa.nome is None or pessoa.apelido is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Pessoa nome or apelido can't be null or empty.",
        )
    instance = create_pessoa(db=db, pessoa=pessoa)
    headers = {"Location": "http://localhost:9999/pessoas/{id}".format(id=instance.id)}
    return JSONResponse(
        content=jsonable_encoder(PessoaSchema.model_validate(instance)),
        status_code=status.HTTP_201_CREATED,
        headers=headers,
    )


@router.get(
    "/pessoas/{id}", status_code=status.HTTP_200_OK, response_model=PessoaSchema
)
async def get_by_id(id: int, db: Session = Depends(get_db)):
    instance = get_pessoa_by_id(db=db, pessoa_id=id)
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pessoa not found"
        )
    return instance


@router.get("/contagem-pessoas", status_code=status.HTTP_200_OK, response_model=int)
async def get_by_id(db: Session = Depends(get_db)):
    return count_pessoas(db=db)


@router.put(
    "/pessoas/{id}", status_code=status.HTTP_200_OK, response_model=PessoaSchema
)
async def update_by_id(id: int, pessoa: PessoaSchema, db: Session = Depends(get_db)):
    instance = update_pessoa(db=db, pessoa_id=id, changes=pessoa)
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pessoa not found"
        )
    return instance


@router.delete("/pessoas/{id}", status_code=status.HTTP_200_OK, response_model=None)
async def delete_by_id(id: int, db: Session = Depends(get_db)):
    instance = remove_pessoa(db=db, pessoa_id=id)
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pessoa not found"
        )
    return {"message": "Pessoa deleted"}
