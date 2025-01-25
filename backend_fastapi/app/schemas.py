from typing import Set, Optional
from pydantic import BaseModel, ConfigDict, field_validator, constr
from datetime import datetime
from pydantic_core import PydanticCustomError


class PessoaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[str] = None
    nome: Optional[constr(max_length=100)] = None
    apelido: Optional[constr(max_length=32)] = None
    nascimento: constr(max_length=10)
    stack: Optional[Set[constr(max_length=32)]] = None

    @field_validator("nascimento")
    @classmethod
    def str_date_must_be_valid(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError as e:
            raise PydanticCustomError(
                "the_answer_error",
                "{nascimento} is not a valid date!",
                {"nascimento": v},
            )

        return v
