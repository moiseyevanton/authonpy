from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os

import models.models as models
from db.db import get_db

SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY") 
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "24"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=int(ACCESS_TOKEN_EXPIRE_HOURS))
    to_encode.update({"exp": int(expire.timestamp())})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)
    full_name = payload.get("sub")
    role = payload.get("role")
    user_id = payload.get("user_id")

    if not full_name or not role or not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # Загружаем пользователя из нужной таблицы
    if role == "employer":
        user = db.query(models.Employer).filter(models.Employer.ID_employer == user_id).first()
    elif role == "administrator":
        user = db.query(models.Administrator).filter(models.Administrator.ID_administrator == user_id).first()
    elif role == "worker":
        user = db.query(models.Worker).filter(models.Worker.ID_worker == user_id).first()
    else:
        raise HTTPException(status_code=401, detail="Invalid role")

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    # Присоединяем роль к объекту для удобства
    user.role = role
    return user