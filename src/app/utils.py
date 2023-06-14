import os
from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User

ALGORITHM = os.getenv('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
JWT_SECRET_KEY = str(os.getenv('JWT_SECRET_KEY'))

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any]) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


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
