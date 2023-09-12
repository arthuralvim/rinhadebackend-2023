from app.models.base import Base
from fastapi import HTTPException, status
from sqlalchemy import Column, Integer, String, select, Text, Computed, Index
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func as F
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.types import ARRAY
from sqlalchemy import text


class Person(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    apelido = Column(String(32), unique=True, nullable=False)
    nascimento = Column(String(10), nullable=False)
    stack = Column(ARRAY(String(32)), nullable=True)
    search = Column(Text, Computed("nome || apelido || stack"))

    __tablename__ = "pessoas"
    __table_args__ = (
        Index(
            "idx_search",
            "search",
            postgresql_using="gist",
            postgresql_ops={"search": "gist_trgm_ops"},
        ),
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    async def count(cls, db_session: AsyncSession):
        """
        :param db_session:
        :return:
        """
        try:
            # stmt = select(cls.id).count()
            return await db_session.scalar(select(F.count()).select_from(cls))
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex

    @classmethod
    async def find_by_id(
        cls, db_session: AsyncSession, person_id: int, raise_http_error=True
    ):
        """
        :param db_session:
        :param person_id:
        :return:
        """
        stmt = select(cls).where(cls.id == person_id)
        result = await db_session.execute(stmt)
        instance = result.scalars().first()
        if instance is None and raise_http_error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"Not found": f"There is no record for id: {person_id}"},
            )
        else:
            return instance

    @classmethod
    async def delete_by_id(
        cls, db_session: AsyncSession, person_id: int, raise_http_error=True
    ):
        """
        :param db_session:
        :param person_id:
        :return:
        """
        was_deleted = False
        instance = await cls.find_by_id(
            db_session=db_session,
            person_id=person_id,
            raise_http_error=raise_http_error,
        )
        if instance:
            was_deleted = await instance.delete(db_session)
        return was_deleted

    @classmethod
    async def update_by_id(
        cls, db_session: AsyncSession, person_id: int, raise_http_error=True, **kwargs
    ):
        """
        :param db_session:
        :param person_id:
        :return:
        """
        instance = await cls.find_by_id(
            db_session=db_session,
            person_id=person_id,
            raise_http_error=raise_http_error,
        )
        if instance:
            instance_updated = await instance.update(db_session, **kwargs)
        return instance_updated

    @classmethod
    async def search_by_term(cls, db_session: AsyncSession, search_term: str):
        """
        :param db_session:
        :param search_term:
        :return:
        """
        stmt = select(cls).where(cls.search.ilike(f"%{search_term}%")).limit(50)

        result = await db_session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def list(cls, db_session: AsyncSession, skip: int = 0, limit: int = 100):
        """
        :param db_session:
        :param skip:
        :param limit:
        :return:
        """
        stmt = select(cls).offset(skip).limit(limit)
        result = await db_session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def nick_already_exists(
        cls, db_session: AsyncSession, nick: str, raise_http_error=True
    ):
        """
        :param db_session:
        :param apelido:
        :return:
        """
        stmt = select(cls).where(cls.apelido == nick)
        result = await db_session.execute(stmt)
        instance = result.scalars().first()
        if instance is not None and raise_http_error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nick taken by other person.",
                # detail={"Not found": f"There is no record for apelido: {apelido}"},
            )

    @classmethod
    async def table_exists(cls, db_session: AsyncSession):
        """
        :param db_session:
        :return:
        """
        stmt = text(
            """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'pessoas'
        );
        """
        )
        result = await db_session.execute(stmt)
        return result.scalars().one()

    @classmethod
    async def list_extensions(cls, db_session: AsyncSession):
        """
        :param db_session:
        :return:
        """
        stmt = text("SELECT * FROM pg_extension;")
        result = await db_session.execute(stmt)
        return result.scalars()
