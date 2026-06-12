

from app.limiter import limiter
from slowapi.util import get_remote_address
from fastapi import Request
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.schemas import UserCreate, UserResponse, Token, VerifyRequest, ForgotPassword, ResetPassword
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import register_user, verify_password, create_access_token, create_refresh_token, get_password_hash
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timezone
from app.models.models import User, RefreshToken
from app.services.email_service import send_reset_email
import random

class RefreshTokenRequest(BaseModel):
    refresh_token: str


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def auth_register(
    create_user: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(
        db,
        create_user.email,
        create_user.password,
    )
    
@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def auth_login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="email was not found")
    
    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="password was not verified")
    
    token = create_access_token(data={"sub": db_user.email})
    refresh_token = create_refresh_token(db, db_user.id)
    return Token(access_token=token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh", response_model=Token)
async def autho_refresh(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    token = db.query(RefreshToken).filter(RefreshToken.token == request.refresh_token).first()
    if not token:
        raise HTTPException(status_code=401, detail="token was not founded")

    if token.is_revoked:
        raise HTTPException(status_code=401, detail="token was revoked")
    
    if token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="token was expired")
    
    user = db.query(User).filter(User.id == token.user_id).first()
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(db, token.user_id)
    return Token(access_token=access_token, refresh_token=request.refresh_token, token_type="bearer")

@router.post("/verify", response_model=UserResponse)
async def autho_verify(
    request: VerifyRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Email was not founds")
    
    if user.verification_code != request.code:
        raise HTTPException(status_code=401, detail="password was not verified")
    
    user.is_verified = True
    user.is_active = True
    user.verification_code = None
    db.commit()
    db.refresh(user)
    return user

@router.post("/forgot-password", response_model=UserResponse)
async def forgot_password(
    request: ForgotPassword,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="user was not founded")
    code = str(random.randint(10000, 99999))
    user.reset_code = code
    db.commit()
    db.refresh(user)
    send_reset_email(user.email, code)
    return user

@router.post("/reset-password", response_model=UserResponse)
async def autho_reset(
    request: ResetPassword,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="user was not founded")
    
    if user.reset_code != request.code:
        raise HTTPException(status_code=400, detail="Invalid code")
    user.hashed_password = get_password_hash(request.new_password)
    user.reset_code = None
    db.commit()
    db.refresh(user)
    return user