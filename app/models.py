from sqlalchemy import Column, Integer, String
from sqlalchemy.types import ARRAY
from app.config import Base


class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    apelido = Column(String(32), unique=True, nullable=False)
    nascimento = Column(String(10), nullable=False)
    stack = Column(ARRAY(String(32)), nullable=True)
