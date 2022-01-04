from fastapi import Depends
from ..settings import SECRET_KEY
from .settings import OAUTH2_SCHEMA, ALGORITHM, CREDENTIALS_EXCEPTION

# JWT
from jose import jwt, JWTError

# DB
from ..database import database
from ..users.models import User

# Schemas
from .schemas import TokenData


def verify_token(token: str = Depends(OAUTH2_SCHEMA)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise CREDENTIALS_EXCEPTION
        return TokenData(username=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION


async def get_current_user(token_data: str = Depends(verify_token)):
    query = User.select().where(User.c.username == token_data.username)
    user = await database.fetch_one(query)
    if not user:
        raise CREDENTIALS_EXCEPTION
    return user
