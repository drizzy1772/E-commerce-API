






from uuid import uuid4
from app.database import get_db
from app.models.models import User, RefreshToken
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from app.config import settings
import secrets
from app.services.email_service import send_welcome_email
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import random


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

pwd_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(db: Session, user_id: int):
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = RefreshToken(token=token, user_id=user_id, expires_at=expires_at)
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return token

def register_user(db: Session, email: str, password: str):
    code = str(random.randint(10000, 999999))

    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="email exists")
    hashed = get_password_hash(password)
    user = User(
        email=email,
        hashed_password=hashed,
        verification_code=code
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    send_welcome_email(user.email, code)
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email = payload.get("sub")
            if not email:
                raise HTTPException(status_code=401, detail="Invalid email")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
