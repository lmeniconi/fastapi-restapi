from pydantic import BaseModel, Field

from typing import Optional

from ..users.schemas import username, password


class LoginSchema(BaseModel):
    username: str = username
    password: str = password


class TokenSchema(BaseModel):
    access_token: str = Field(..., title="Access Token",
                              description="The Access Token")
    token_type: str = Field(..., title="Access Token Type",
                            description="The type of the Token")


class TokenData(BaseModel):
    username: Optional[str] = None
