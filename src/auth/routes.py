from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

# Schemas
from .schemas import LoginTokenSchema

# Utils
from .utils import authenticate_user, create_access_token

router = APIRouter(
    prefix='',
    tags=['Auth']
)


@router.post('/login', response_model=LoginTokenSchema)
async def login(request: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(request.username, request.password)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
