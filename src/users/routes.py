from fastapi import APIRouter, Body, status, Depends, Path
from typing import List

# DB
from ..database import database
from .models import User

# Schemas
from .schemas import UserSchema, CreateUserSchema
from ..auth.schemas import TokenSchema

# Depends
from ..auth.depends import verify_token
from .depends import is_creator

# Passwords
from passlib.hash import pbkdf2_sha256

# Utils
from .utils import get_user_db, user_is_valid

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.get('/', response_model=List[UserSchema])
async def get_users(token: TokenSchema = Depends(verify_token)):
    query = User.select()
    return await database.fetch_all(query)


@router.get('/{id}', response_model=UserSchema)
async def get_user(id: int = Path(..., gt=0), token: TokenSchema = Depends(verify_token)):
    return await get_user_db(id)


@router.post('/', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: CreateUserSchema = Body(...)):
    await user_is_valid(user_data)
    hashed_password = pbkdf2_sha256.hash(user_data.password)
    query = User.insert().values(username=user_data.username, password=hashed_password)
    response_id = await database.execute(query)
    return {"id": response_id, **user_data.dict()}


@router.put('/{id}', response_model=UserSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_data: CreateUserSchema = Body(...), user: UserSchema = Depends(is_creator)):
    await user_is_valid(user_data)
    hashed_password = pbkdf2_sha256.hash(user_data.password)
    query = User.update().where(User.c.id == user.id).values(
        username=user_data.username, password=hashed_password)
    await database.execute(query)
    return {'id': user.id, **user_data.dict()}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: UserSchema = Depends(is_creator)):
    query = User.delete().where(User.c.id == user.id)
    await database.execute(query)
