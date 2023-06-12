from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .utils import verify_password


async def authenticate_user(
    session: AsyncSession,
    username: str,
    password: str
):
    result = await session.scalars(
        select(User).where(User.username==username)
    )
    user = result.first()
    if user and verify_password(password, user.hashed_password):
        return user
