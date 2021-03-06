from fastapi import Depends, HTTPException, status, Path, Body

from ..database import database

from ..auth.depends import get_current_user

from .models import User

from .schemas import UserSchema, CreateUserSchema

from .utils import get_user_db


async def is_creator(id: int = Path(..., gt=0), current_user: UserSchema = Depends(get_current_user)):
    user = await get_user_db(id)
    if not user.id == current_user.id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return user


async def user_is_valid_create(user_data: CreateUserSchema = Body(...)):
    query = User.select().where(User.c.username == user_data.username)
    user = await database.fetch_one(query)
    if user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="username has already be taken")


async def user_is_valid_update(user_data: CreateUserSchema = Body(...), current_user: UserSchema = Depends(get_current_user)):
    query = User.select().where(User.c.username == user_data.username)
    user = await database.fetch_one(query)
    if user:
        if user.username != current_user.username:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="username has already be taken")
