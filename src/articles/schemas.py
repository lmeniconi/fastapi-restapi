from pydantic import BaseModel, Field

title = Field(..., title='Title',
              description='Title of the article', max_length=100)
description = Field(..., title='Description',
                    description='Description of the article', max_length=500)


class ArticleSchema(BaseModel):
    id: int = Field(...)
    title: str = title
    description: str = description
    user_id: int = Field(...)


class CreateArticleSchema(BaseModel):
    title: str = title
    description: str = description
