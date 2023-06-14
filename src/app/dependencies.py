import os
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import get_user
from database import get_async_session

from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/jwt")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
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
            algorithms=[os.getenv('JWT_ALGORITHM')]
        )
    except JWTError:
        raise credentials_exception
    else:
        username = payload.get("sub")
        user = await get_user(session, username)
        if user:
            return user
        else:
            raise credentials_exception


async def get_current_owner_user(
    current_user: Annotated[User, Depends(get_current_user)],
    username: Annotated[str, Path()],
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    user = await get_user(session, username)
    if user and current_user.username == user.username:
        return current_user

    elif user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"User '{username}' doesnt't exist"
        )
    elif current_user.username != user.username:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=f"You don't have permission"
        )
