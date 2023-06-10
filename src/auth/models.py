from typing import Annotated

from fastapi import Depends
from fastapi_users.db import (SQLAlchemyBaseUserTableUUID,
                              SQLAlchemyUserDatabase)
from sqlalchemy import Column, String

from database import AsyncSession, Base, get_async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    
    username = Column(String(50), nullable=False, unique=True)


async def get_user_db(session: Annotated[AsyncSession, Depends(get_async_session)]):
    yield SQLAlchemyUserDatabase(session, User)
