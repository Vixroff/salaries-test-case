from typing import Annotated

import fastapi_users
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from .manager import UserManager
from .models import User


async def get_user_db(session: Annotated[AsyncSession, Depends(get_async_session)]):
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db: Annotated[SQLAlchemyUserDatabase, Depends(get_user_db) ]):
    yield UserManager(user_db)

current_user = fastapi_users.current_user()


