from sqlalchemy.orm import Session
from sqlalchemy import or_, func as F
from app.models import Pessoa
from app.schemas import PessoaSchema
from typing import Optional


def get_pessoas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pessoa).offset(skip).limit(limit).all()


def count_pessoas(db: Session):
    return db.query(Pessoa).count()


def get_pessoa_by_apelido(db: Session, pessoa: PessoaSchema):
    return db.query(Pessoa).filter(Pessoa.apelido == pessoa.apelido).first()


def search_pessoas(db: Session, search_term: Optional[str]):
    if not search_term:
        return None

    return (
        db.query(Pessoa)
        .filter(
            or_(
                # Pessoa.apelido.match(search_term),
                Pessoa.apelido.ilike(f"%{search_term}%"),
                # Pessoa.nome.match(search_term),
                Pessoa.nome.ilike(f"%{search_term}%"),
                # F.array_to_string(Pessoa.stack, ",").match(search_term),
                F.array_to_string(Pessoa.stack, ",").ilike(f"%{search_term}%"),
            )
        )
        .limit(50)
        .all()
    )


def get_pessoa_by_id(db: Session, pessoa_id: int):
    return db.get(Pessoa, pessoa_id)


def create_pessoa(db: Session, pessoa: PessoaSchema):
    instance = Pessoa(
        nome=pessoa.nome,
        apelido=pessoa.apelido,
        nascimento=pessoa.nascimento,
        stack=pessoa.stack,
    )
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def remove_pessoa(db: Session, pessoa_id: int):
    instance = get_pessoa_by_id(db, pessoa_id)
    if not instance:
        return None
    db.delete(instance)
    db.commit()


def update_pessoa(db: Session, pessoa_id: int, changes: dict):
    instance = get_pessoa_by_id(db, pessoa_id)
    if not instance:
        return None
    for field, value in changes.items():
        if hasattr(instance, field):
            setattr(instance, field, value)
    db.commit()
    db.refresh(instance)
    return instance
