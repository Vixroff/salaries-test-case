from fastapi import APIRouter

from .auth import auth_backend, fastapi_users
from .schemas import UserCreate, UserRead

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
