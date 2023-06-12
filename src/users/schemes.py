from pydantic import UUID4, BaseModel, Field


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

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

