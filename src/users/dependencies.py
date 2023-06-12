from typing import Annotated
from http import HTTPStatus
import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from database import get_async_session

from .models import User
from .utils import verify_password

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            str(os.getenv('JWT_SECRET_KEY')),
            algorithms=[ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    result = await session.scalars(
        select(User).where(User.username==username)
    )
    user = result.first()
    if user is None:
        raise credentials_exception
    return user
