from fastapi import APIRouter, Body, status, Depends, Path
from typing import List

# DB
from ..database import database
from .models import User

# Schemas
from .schemas import UserSchema, CreateUserSchema

# Depends
from ..auth.depends import verify_token
from .depends import is_creator, user_is_valid_create, user_is_valid_update

# Passwords
from passlib.hash import pbkdf2_sha256

# Utils
from .utils import get_user_db

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.get('/', dependencies=[Depends(verify_token)], response_model=List[UserSchema])
async def get_users():
    query = User.select()
    return await database.fetch_all(query)


@router.get('/{id}', dependencies=[Depends(verify_token)], response_model=UserSchema)
async def get_user(id: int = Path(..., gt=0)):
    return await get_user_db(id)


@router.post('/', dependencies=[Depends(user_is_valid_create)], response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: CreateUserSchema = Body(...)):
    hashed_password = pbkdf2_sha256.hash(user_data.password)
    query = User.insert().values(username=user_data.username, password=hashed_password)
    response_id = await database.execute(query)
    return {"id": response_id, **user_data.dict()}


@router.put('/{id}', dependencies=[Depends(user_is_valid_update), Depends(is_creator)], response_model=UserSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_user(id: int = Path(..., gt=0), user_data: CreateUserSchema = Body(...)):
    hashed_password = pbkdf2_sha256.hash(user_data.password)
    query = User.update().where(User.c.id == id).values(
        username=user_data.username, password=hashed_password)
    await database.execute(query)
    return {'id': id, **user_data.dict()}


@router.delete('/{id}', dependencies=[Depends(is_creator)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int = Path(..., gt=0)):
    query = User.delete().where(User.c.id == id)
    await database.execute(query)
