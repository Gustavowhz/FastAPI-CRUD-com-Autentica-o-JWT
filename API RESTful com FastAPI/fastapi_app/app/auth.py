from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import crud, models, database
from .database import get_db
from app import auth

SECRET_KEY = "segredo"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def criar_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise cred_exception
    except JWTError:
        raise cred_exception

    user = crud.get_usuario_by_email(db, email=email)
    if user is None:
        raise cred_exception
    return user
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = auth.verificar_token_jwt(token) 
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )
