import pytest

from app.models import Person
from app.schemas import PessoaSchema

pytestmark = pytest.mark.anyio


class TestHomeReady:
    async def test_home_endpoint(self, client):
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"hello": "welcome home"}

    async def test_ready_when_not_ready(self, client):
        response = await client.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"ready": False}

    async def test_ready_when_ready(self, client, db_session):
        await Person.list_extensions(db_session)
        response = await client.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"ready": True}
