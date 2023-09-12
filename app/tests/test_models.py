import pytest

from app.models import Person
from app.schemas import PessoaSchema

pytestmark = pytest.mark.anyio


@pytest.fixture
def person(pessoa_):
    pessoa = PessoaSchema(**pessoa_)
    return Person(
        nome=pessoa.nome,
        apelido=pessoa.apelido,
        nascimento=pessoa.nascimento,
        stack=pessoa.stack,
    )


@pytest.fixture
def persons(pessoa_):
    pessoa = PessoaSchema(**pessoa_)
    persons = []
    for i in range(5):
        persons.append(
            Person(
                nome=pessoa.nome,
                apelido=pessoa.apelido + str(i),
                nascimento=pessoa.nascimento,
                stack=pessoa.stack,
            )
        )
    return persons


class TestPersonCRUD:
    async def test_should_create_and_retrieve_person(self, db_session, person):
        person = await person.save(db_session)
        person_instance = await Person.find_by_id(db_session, person_id=person.id)
        assert person.id == person_instance.id

    async def test_should_remove_person(self, db_session, person):
        person = await person.save(db_session)
        was_deleted = await Person.delete_by_id(db_session, person_id=person.id)
        assert was_deleted
        person_instance = await Person.find_by_id(
            db_session, person_id=person.id, raise_http_error=False
        )
        assert person_instance is None

        async def test_should_update_person(self, db_session, person):
            person = await person.save(db_session)
            person_update = await Person.update_by_id(
                db_session, person_id=person.id, nome="Bruce Wayne da Silva"
            )
            assert person_update.nome == "Bruce Wayne da Silva"
            person_update = await person.update_by_id(
                db_session, person_id=person.id, stack=["c++", "python"]
            )
            assert len(person_update.stack) == 2

    async def test_should_not_remove_person_that_doesnt_exist(self, db_session):
        deleted = await Person.delete_by_id(
            db_session, person_id=1, raise_http_error=False
        )
        assert not deleted

        async def test_should_not_update_person_that_doesnt_exist(self, db_session):
            person_update = await Person.update_by_id(
                db_session, person_id=1, stack=["c++", "python"]
            )
            assert person_update is None

    async def test_should_not_retrieve_person_that_doesnt_exist(self, db_session):
        person = await Person.find_by_id(
            db_session, person_id=1, raise_http_error=False
        )
        assert person is None


class TestPersonQuery:
    async def test_get_list_persons(self, db_session, persons):
        persons_list = await Person.list(db_session)
        assert len(persons_list) == 0

        for person in persons:
            await person.save(db_session)

        persons_list = await Person.list(db_session)
        assert len(persons_list) == 5

    async def test_count_persons(self, db_session, persons):
        count = await Person.count(db_session)
        assert count == 0

        for person in persons:
            await person.save(db_session)

        count = await Person.count(db_session)
        assert count == 5


class TestPersonSearch:
    async def test_search_persons_by_nick(self, db_session, persons):
        for person in persons:
            await person.save(db_session)

        persons_search_list = await Person.search_by_term(
            db_session, search_term="batman"
        )
        assert len(persons_search_list) == 5

    async def test_search_persons_by_name(self, db_session, persons):
        for person in persons:
            await person.save(db_session)

        persons_search_list = await Person.search_by_term(
            db_session, search_term="bruce"
        )
        assert len(persons_search_list) == 5

    async def test_search_persons_by_stack(self, db_session, persons):
        for person in persons:
            person.stack = ["python", "c++"]
            await person.save(db_session)

        persons_search_list = await Person.search_by_term(db_session, search_term="++")
        assert len(persons_search_list) == 5
