from fastapi import FastAPI

# Routes
from src.users.routes import router as users_router
from src.auth.routes import router as auth_router
from src.articles.routes import router as articles_router

# Models
from src.users.models import metadata as users_metadata
from src.articles.models import metadata as articles_metadata

# DB Setup
from src.database import database, engine
users_metadata.create_all(engine)
articles_metadata.create_all(engine)

# APP
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()
    print('Connected')


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    print('Disconnected')

# Routes
routers = [users_router, auth_router, articles_router]
for router in routers:
    app.include_router(router)
