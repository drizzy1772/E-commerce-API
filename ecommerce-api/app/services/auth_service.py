






from uuid import uuid4
from app.database import get_db
from app.models.models import User, RefreshToken, UserRole
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from jose import jwt
from pwdlib import PasswordHash
from datetime import datetime, timezone, timedelta
from app.config import settings
import secrets
from app.services.email_service import send_welcome_email
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import auth_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

pwd_context = PasswordHash.recommended()

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def create_refresh_token(db: AsyncSession, user_id: int):
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    await auth_repository.create_refresh_token(db, token, user_id, expires_at)
    return token

async def register_user(db: AsyncSession, email: str, password: str):
    code = str(random.randint(10000, 999999))
    user = await auth_repository.get_user_by_email(db, email)
    
    if user:
        raise HTTPException(status_code=400, detail="email exists")
    hashed = get_password_hash(password)
    user = await auth_repository.create_user(db, email, hashed, code)
    return user, code

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email = payload.get("sub")
            if not email:
                raise HTTPException(status_code=401, detail="Invalid email")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await auth_repository.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user


def require_admin(current_user: User = Depends(get_current_user)):
    
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Admin access required")
    return current_user