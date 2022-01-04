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
