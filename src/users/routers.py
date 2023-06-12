from http import HTTPStatus
from typing import Annotated

from fastapi import Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from main import app

from .models import User
from .dependencies import authenticate_user
from .schemes import UserIn, UserOut, Token
from .utils import get_hashed_password, create_access_token


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserOut)
async def create_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[UserIn, Body()]
):
    new_user = User(
        username=user.username,
        hashed_password=get_hashed_password(user.password)
    )
    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=f"User with username '{user.username}' already exists"
        )


@app.post('/auth/jwt', status_code=HTTPStatus.OK, response_model=Token)
async def login_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if user:
        return {
            "access_token": create_access_token(user.username),
            "token_type": "bearer"
        }
    else:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
