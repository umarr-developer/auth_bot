from datetime import datetime

from sqlalchemy import (BigInteger, Boolean, Column, Date, Integer, Sequence,
                        insert, select, update)
from src.service.database import Base, sessionmaker


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('id'))
    user_id = Column(BigInteger, primary_key=True)
    created_on = Column(Date, default=datetime.now)
    update_on = Column(Date, default=datetime.now, onupdate=datetime.now)

    @classmethod
    async def new(cls, db_session: sessionmaker, user_id: int) -> tuple['User']:
        sql = insert(cls).values(user_id=user_id)
        async with db_session() as session:
            await session.execute(sql)
            await session.commit()
        return await cls.get(db_session, user_id=user_id)

    @classmethod
    async def get(cls, db_session: sessionmaker, user_id: int) -> tuple['User']:
        sql = select(cls).where(cls.user_id == user_id)
        async with db_session() as session:
            response = await session.execute(sql)
        return response.fetchone()
