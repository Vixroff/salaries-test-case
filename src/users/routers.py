from typing import Annotated
from http import HTTPStatus

from fastapi import Depends, Body, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from database import get_async_session

from .schemes import UserIn, UserOut
from .models import Employee
from .utils import get_hashed_password


@app.post('users/', status_code=HTTPStatus.CREATED, response_model=UserOut)
async def create_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[UserIn, Body()]
):
    new_user = Employee(
        username=user.username,
        hashed_password=get_hashed_password(user.password)
    )
    session.add(new_user)
    try:
        await session.commit()
        return user
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=f'User with username {user.username} already exists'
        )
    


    
