from pydantic import BaseModel, Field, UUID4


class UserIn(BaseModel):
    username: str = Field(
        max_length=50,
    )
    password: str = Field(
        min_length=8,
        max_length=50,
    )


class UserOut(BaseModel):
    id: UUID4
    username: str
