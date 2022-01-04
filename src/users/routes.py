from fastapi import APIRouter, Body, status
from typing import List

# DB
from ..database import database
from .models import User

# Schemas
from .schemas import UserSchema, CreateUserSchema

# Passwords
from passlib.hash import pbkdf2_sha256

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.get('/', response_model=List[UserSchema])
async def get_users():
    query = User.select()
    return await database.fetch_all(query)


@router.post('/', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUserSchema = Body(...)):
    hashed_password = pbkdf2_sha256.hash(user.password)
    query = User.insert().values(username=user.username, password=hashed_password)
    response_id = await database.execute(query)
    return {"id": response_id, **user.dict()}
