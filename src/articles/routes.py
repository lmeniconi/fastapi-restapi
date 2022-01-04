from fastapi import APIRouter, Body, Path, HTTPException, status, Depends
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


from typing import List

# DB
from ..database import database
from .models import Article

# Schemas
from .schemas import ArticleSchema, CreateArticleSchema
from ..users.schemas import UserSchema

# Dependencies
from ..auth.dependencies import verify_token

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
    query = Article.select().where(Article.c.id == id)
    article = await database.fetch_one(query)
    if not article:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return article


@router.post('/', response_model=ArticleSchema, status_code=status.HTTP_201_CREATED)
async def create_article(article: CreateArticleSchema = Body(...)):
    query = Article.insert().values(title=article.title,
                                    description=article.description)
    response_id = await database.execute(query)
    return {"id": response_id, **article.dict()}


@router.put('/{id}', response_model=ArticleSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_article(id: int = Path(..., gt=0), article: CreateArticleSchema = Body(...)):
    query = Article.update().where(Article.c.id == id).values(
        title=article.title, description=article.description)
    response_id = await database.execute(query)
    if not response_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return {"id": id, **article.dict()}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(id: int = Path(..., gt=0)):
    query = Article.delete().where(Article.c.id == id)
    response_id = await database.execute(query)
    if not response_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
