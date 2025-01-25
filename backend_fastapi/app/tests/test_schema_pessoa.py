import pytest
from app.schemas import PessoaSchema
from pydantic import ValidationError


class TestSchemaPessoa:
    def test_create_pessoa(self, pessoa_):
        pessoa = PessoaSchema(**pessoa_)
        assert pessoa.id is None
        assert pessoa.nome == "bruce wayne da silva"
        assert pessoa.apelido == "batman"
        assert pessoa.nascimento == "1979-04-20"
        assert pessoa.stack is None

    def test_should_create_pessoa_using_minimal_payload(self):
        with pytest.raises(ValidationError):
            pessoa = PessoaSchema()

        pessoa = PessoaSchema(nome="Fast", apelido="Furious", nascimento="2000-01-01")
        assert pessoa.id is None
        assert pessoa.nome == "Fast"
        assert pessoa.apelido == "Furious"
        assert pessoa.nascimento == "2000-01-01"
        assert pessoa.stack is None

    def test_should_raise_validation_error_when_date_is_invalid(self):
        with pytest.raises(ValidationError):
            pessoa = PessoaSchema(
                nome="Fast", apelido="Furious", nascimento="2000-13-01"
            )

    def test_stack_should_not_have_repeated_values(self, pessoa_):
        pessoa = PessoaSchema(**pessoa_, stack=["python", "python"])
        assert len(pessoa.stack) == 1

    def test_create_pessoa_with_stack(self, pessoa_):
        pessoa = PessoaSchema(**pessoa_, stack=["python"])
        assert "python" in pessoa.stack
        assert "c++" not in pessoa.stack
        pessoa.stack.add("c++")
        assert "c++" in pessoa.stack

    def test_should_raise_validation_error_when_length_constraint(self, pessoa_):
        with pytest.raises(ValidationError):
            pessoa = PessoaSchema(
                **{
                    "nome": "p" * 101,
                    "apelido": "p",
                    "nascimento": "2000-10-01",
                    "stack": ["C#", "Node", "Oracle"],
                }
            )

        with pytest.raises(ValidationError):
            pessoa = PessoaSchema(
                **{
                    "nome": "p",
                    "apelido": "p" * 33,
                    "nascimento": "2000-10-01",
                    "stack": ["C#", "Node", "Oracle"],
                }
            )

        with pytest.raises(ValidationError):
            pessoa = PessoaSchema(
                **{
                    "nome": "p",
                    "apelido": "p",
                    "nascimento": "2000-10-01",
                    "stack": ["p" * 33, "Node", "Oracle"],
                }
            )
