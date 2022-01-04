from fastapi import Depends, HTTPException, status, Path

from ..auth.depends import get_current_user

from .schemas import ArticleSchema
from ..users.schemas import UserSchema

from .utils import get_article_db


async def is_creator(id: int = Path(...), user: UserSchema = Depends(get_current_user)):
    article = await get_article_db(id)
    if not article.user_id == user.id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return user
