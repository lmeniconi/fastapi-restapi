from datetime import datetime, timedelta
from fastapi import HTTPException, status

# JWT
from jose import jwt

# Settings
from ..settings import SECRET_KEY
from .settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

# DB
from ..database import database
from ..users.models import User

# Password
from passlib.hash import pbkdf2_sha256


async def authenticate_user(username: str, password: str):
    query = User.select().where(User.c.username == username)
    user = await database.fetch_one(query)

    if not user or not pbkdf2_sha256.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
