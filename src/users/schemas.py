from pydantic import BaseModel, Field

username = Field(..., min_length=1, max_length=20)
password = Field(..., min_length=6, max_length=50)


class UserSchema(BaseModel):
    id: int = Field(...)
    username: str = username


class CreateUserSchema(BaseModel):
    username: str = username
    password: str = password
