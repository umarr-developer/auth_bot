from sqlalchemy import JSON, Column, Integer, Sequence, String, select

from src.service.database import Base, sessionmaker


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, Sequence('id'), primary_key=True)
    photo_id = Column(String, default=None)
    description = Column(String)
    answers = Column(JSON)

    @classmethod
    async def get(cls, db_session: sessionmaker, id: int) -> tuple['Question']:
        sql = select(cls).where(cls.id == id)
        async with db_session() as session:
            response = await session.execute(sql)
        return response.fetchone()

    @classmethod
    async def all(cls, db_session: sessionmaker) -> list[tuple['Question']]:
        sql = select(cls)
        async with db_session() as session:
            response = await session.execute(sql)
        return response.fetchall()
