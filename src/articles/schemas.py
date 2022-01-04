from pydantic import BaseModel, Field

title = Field(..., title='Title',
              description='Title of the article', max_length=100)
description = Field(..., title='Description',
                    description='Description of the article', max_length=500)


class ArticleSchema(BaseModel):
    id: int = Field(...)
    title: str = title
    description: str = description


class CreateArticleSchema(BaseModel):
    title: str = title
    description: str = description
