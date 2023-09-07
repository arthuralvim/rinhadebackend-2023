import pytest

from data import count_pessoas
from data import get_pessoas
from data import create_pessoa
from data import get_pessoa_by_id
from data import remove_pessoa
from data import update_pessoa
from data import search_pessoas
from schemas import PessoaSchema


class TestPessoaCRUD:
    def test_should_create_and_retrieve_pessoa(self, db_session, pessoa_):
        pessoa = create_pessoa(db_session, PessoaSchema(**pessoa_))
        pessoa_instance = get_pessoa_by_id(db_session, pessoa_id=pessoa.id)
        assert pessoa.id == pessoa_instance.id

    def test_should_remove_pessoa(self, db_session, pessoa_):
        pessoa = create_pessoa(db_session, PessoaSchema(**pessoa_))
        remove_pessoa(db_session, pessoa_id=pessoa.id)
        pessoa_instance = get_pessoa_by_id(db_session, pessoa_id=pessoa.id)
        assert pessoa_instance is None

    def test_should_update_pessoa(self, db_session, pessoa_):
        pessoa_schema = PessoaSchema(**pessoa_)
        pessoa = create_pessoa(db_session, pessoa_schema)
        pessoa_updated = update_pessoa(
            db_session, pessoa_id=pessoa.id, changes={"nome": "Bruce Wayne da Silva"}
        )
        assert pessoa_updated.nome == "Bruce Wayne da Silva"
        pessoa_updated = update_pessoa(
            db_session, pessoa_id=pessoa.id, changes={"stack": ["c++", "python"]}
        )
        assert len(pessoa_updated.stack) == 2

    def test_should_remove_pessoa_that_doesnt_exist(self, db_session, pessoa_):
        pessoa_removed = remove_pessoa(db_session, pessoa_id=10)
        assert pessoa_removed is None

    def test_should_update_pessoa_that_doesnt_exist(self, db_session, pessoa_):
        pessoa_updated = update_pessoa(
            db_session, pessoa_id=10, changes={"stack": ["c++", "python"]}
        )
        assert pessoa_updated is None

    def test_should_retrieve_pessoa_that_doesnt_exist(self, db_session, pessoa_):
        pessoa_instance = get_pessoa_by_id(db_session, pessoa_id=10)
        assert pessoa_instance is None


class TestPessoaQuery:
    def test_get_pessoas(self, db_session, pessoa_):
        pessoas = get_pessoas(db_session)
        assert len(pessoas) == 0
        for i in range(5):
            pessoa_.update({"apelido": "batman" + str(i)})
            pessoa = create_pessoa(db_session, PessoaSchema(**pessoa_))

        pessoas = get_pessoas(db_session)
        assert len(pessoas) == 5

    def test_count_pessoas(self, db_session, pessoa_):
        count = count_pessoas(db_session)
        assert count == 0
        for i in range(5):
            pessoa_.update({"apelido": "batman" + str(i)})
            pessoa = create_pessoa(db_session, PessoaSchema(**pessoa_))
        count = count_pessoas(db_session)
        assert count == 5


class TestPessoaSearch:
    def test_search_pessoas_by_apelido(self, db_session, pessoa_):
        for i in range(5):
            pessoa_.update({"apelido": "batman" + str(i)})
            pessoa = create_pessoa(db_session, PessoaSchema(**pessoa_))
        pessoas = search_pessoas(db_session, search_term="batman")
        assert len(pessoas) == 5

    def test_search_pessoas_by_nome(self, db_session, pessoa_):
        for i in range(5):
            pessoa_.update({"apelido": "batman" + str(i)})
            pessoa = create_pessoa(db_session, PessoaSchema(**pessoa_))
        pessoas = search_pessoas(db_session, search_term="bruce")
        assert len(pessoas) == 5

    def test_search_pessoas_by_stack(self, db_session, pessoa_):
        for i in range(5):
            pessoa_.update({"apelido": "batman" + str(i), "stack": ["python", "c++"]})
            pessoa = create_pessoa(db_session, PessoaSchema(**pessoa_))
        pessoas = search_pessoas(db_session, search_term="++")
        assert len(pessoas) == 5
