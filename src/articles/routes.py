from fastapi import APIRouter, Body, Path, HTTPException, status, Depends

from typing import List

# DB
from ..database import database
from .models import Article

# Schemas
from .schemas import ArticleSchema, CreateArticleSchema
from ..users.schemas import UserSchema

# Dependencies
from ..auth.depends import verify_token, get_current_user
from .depends import is_creator

# Utils
from .utils import get_article_db

router = APIRouter(
    prefix='/articles',
    tags=['Articles'],
    dependencies=[Depends(verify_token)]
)


@router.get('/', response_model=List[ArticleSchema])
async def get_articles():
    query = Article.select()
    return await database.fetch_all(query)


@router.get('/{id}', response_model=ArticleSchema)
async def get_article(id: int = Path(..., gt=0)):
    return await get_article_db(id)


@router.post('/', response_model=ArticleSchema, status_code=status.HTTP_201_CREATED)
async def create_article(article: CreateArticleSchema = Body(...), user: UserSchema = Depends(get_current_user)):
    query = Article.insert().values(title=article.title,
                                    description=article.description,
                                    user_id=user.id)
    response_id = await database.execute(query)
    return {"id": response_id, **article.dict(), "user_id": user.id}


@router.put('/{id}', response_model=ArticleSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_article(id: int = Path(..., gt=0), article: CreateArticleSchema = Body(...), user: UserSchema = Depends(is_creator)):
    query = Article.update().where(Article.c.id == id).values(
        title=article.title, description=article.description)
    await database.execute(query)
    return {"id": id, **article.dict(), "user_id": user.id}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(id: int = Path(..., gt=0), user: int = Depends(is_creator)):
    query = Article.delete().where(Article.c.id == id)
    await database.execute(query)
