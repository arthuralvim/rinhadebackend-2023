import pytest
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import Base


@pytest.fixture
def pessoa_():
    return {
        "nome": "bruce wayne da silva",
        "apelido": "batman",
        "nascimento": "1979-04-20",
    }


@pytest.fixture()
def sqlengine(request):
    """
    Creates a new engine connection with a Postgresql database.
    """

    engine = create_engine(os.environ.get("TEST_DATABASE_URL"), pool_recycle=3600)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def db_session(sqlengine, request):
    """
    Creates a new session/transaction using SQLAlchemy.
    """

    connection = sqlengine.connect()
    transaction = connection.begin()

    session_maker = sessionmaker(bind=connection)
    session = session_maker()

    def teardown():
        session.close()
        transaction.rollback()
        connection.close()

    request.addfinalizer(teardown)

    return session
