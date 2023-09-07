import pytest

from fastapi.testclient import TestClient
from app.main import app
from schemas import PessoaSchema

client = TestClient(app)


class TestEndpoints:
    @pytest.fixture
    def pessoa_1(self):
        return {
            "apelido": "josé",
            "nome": "José Roberto",
            "nascimento": "2000-10-01",
            "stack": ["C#", "Node", "Oracle"],
        }

    @pytest.fixture
    def pessoa_2(self):
        return {
            "apelido": "ana",
            "nome": "Ana Barbosa",
            "nascimento": "1985-09-23",
            "stack": None,
        }

    @pytest.fixture
    def pessoa_3(self):
        return {
            "apelido": "ana",
            "nome": None,  # não pode ser null
            "nascimento": "1985-09-23",
            "stack": None,
        }

    @pytest.fixture
    def pessoa_4(self):
        return {
            "apelido": None,  # não pode ser null
            "nome": "Ana Barbosa",
            "nascimento": "1985-01-23",
            "stack": None,
        }

    @pytest.fixture
    def pessoa_5(self):
        return {
            "apelido": "apelido",
            "nome": 1,  # nome deve ser string e não número
            "nascimento": "1985-01-01",
            "stack": None,
        }

    @pytest.fixture
    def pessoa_6(self):
        return {
            "apelido": "apelido",
            "nome": "nome",
            "nascimento": "1985-01-01",
            "stack": [1, "PHP"],  # stack deve ser um array de apenas strings
        }

    def test_home_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"hello": "welcome home"}

    def test_should_create_pessoas(self, db_session, pessoa_1, pessoa_2):
        response = client.post("/pessoas/", json=pessoa_1)
        assert response.status_code == 201
        response = client.post("/pessoas/", json=pessoa_2)
        assert response.status_code == 201

    def test_should_return_422_when_fail_creating_pessoas(
        self, db_session, pessoa_1, pessoa_3, pessoa_4
    ):
        response = client.post("/pessoas/", json=pessoa_1)
        assert response.status_code == 201
        response = client.post("/pessoas/", json=pessoa_1)
        assert response.status_code == 422

        response = client.post("/pessoas/", json=pessoa_3)
        assert response.status_code == 422

        response = client.post("/pessoas/", json=pessoa_4)
        assert response.status_code == 422

    def test_should_return_400_when_fail_creating_pessoas(
        self, db_session, pessoa_5, pessoa_6
    ):
        response = client.post("/pessoas/", json=pessoa_5)
        assert response.status_code == 400

        response = client.post("/pessoas/", json=pessoa_6)
        assert response.status_code == 400

    def test_should_return_not_found_when_pessoa_doesnt_exist(self, db_session):
        response = client.get("/pessoas/1")
        assert response.status_code == 404

    def test_should_return_pessoa_detail(self, db_session, pessoa_1, pessoa_2):
        response = client.post("/pessoas/", json=pessoa_1)
        assert response.status_code == 201
        pessoa_created = PessoaSchema(**response.json())

        response = client.get(f"/pessoas/{pessoa_created.id}")
        assert response.status_code == 200
        pessoa_retrieved = PessoaSchema(**response.json())

        assert pessoa_created.id == pessoa_retrieved.id
        assert pessoa_created.nome == pessoa_retrieved.nome
        assert pessoa_created.apelido == pessoa_retrieved.apelido
        assert pessoa_created.nascimento == pessoa_retrieved.nascimento

    def test_should_return_search(self, db_session, pessoa_1, pessoa_2):
        response = client.post("/pessoas/", json=pessoa_1)
        assert response.status_code == 201
        response = client.post("/pessoas/", json=pessoa_2)
        assert response.status_code == 201

        response = client.get(f"/pessoas/?t=node")
        assert response.status_code == 200
        pessoas = response.json()
        assert len(pessoas) == 1

        response = client.get(f"/pessoas/?t=berto")
        assert response.status_code == 200
        pessoas = response.json()
        assert len(pessoas) == 1

        response = client.get(f"/pessoas/?t=Python")
        assert response.status_code == 200
        pessoas = response.json()
        assert len(pessoas) == 0

        response = client.get(f"/pessoas/?t=")
        assert response.status_code == 400
