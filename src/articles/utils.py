from fastapi import HTTPException, status

from ..database import database

from .models import Article


async def get_article_db(id: int):
    query = Article.select().where(Article.c.id == id)
    article = await database.fetch_one(query)
    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return article
