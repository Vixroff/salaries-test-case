import uuid

from fastapi_users import models, schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: models.ID
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
