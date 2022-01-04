from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

OAUTH2_SCHEMA = OAuth2PasswordBearer(tokenUrl='/login')

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Cloud not validate credentials",
    headers={'WWW-Authenticate': "Bearer"}
)
