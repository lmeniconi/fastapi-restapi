from fastapi import Depends, HTTPException, status, Path, Body

from ..database import database

from ..auth.depends import get_current_user

from .models import User

from .schemas import UserSchema, CreateUserSchema

from .utils import get_user_db


async def is_creator(id: int = Path(...), current_user: UserSchema = Depends(get_current_user)):
    user = await get_user_db(id)
    if not user.id == current_user.id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return user
