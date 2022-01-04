from fastapi import HTTPException, status

from ..database import database

from .models import User

from .schemas import CreateUserSchema


async def get_user_db(id: int):
    query = User.select().where(User.c.id == id)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return user


async def user_is_valid(user_data: CreateUserSchema):
    query = User.select().where(User.c.username == user_data.username)
    user = await database.fetch_one(query)
    if user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="username has already be taken")
