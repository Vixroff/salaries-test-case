from http import HTTPStatus
from typing import Annotated

from fastapi import Body, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from main import app

from .models import User
from .schemes import UserIn, UserOut
from .utils import get_hashed_password


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
