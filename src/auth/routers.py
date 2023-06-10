import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from .auth import auth_backend
from .dependencies import get_user_manager
from .models import User
from .schemas import UserCreate, UserRead

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


auth_router = APIRouter()

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
