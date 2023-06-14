import os
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from .models import User

ALGORITHM = os.getenv('JWT_ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/jwt")


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


async def get_current_owner_user(
    current_user: Annotated[User, Depends(get_current_user)],
    username: Annotated[str, Path()]
):
    if current_user.username == username:
        return current_user
    else:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=f"You don't have permission"
        )
