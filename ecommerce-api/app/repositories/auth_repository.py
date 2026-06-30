

from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session
from app.models.models import Product, Cart, CartItem, Order, OrderItem, User, RefreshToken



async def get_user_by_email(db, email):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()
    
async def create_user(db, email, hashed_password, code):
    new_user = User(
        email=email,
        hashed_password=hashed_password,
        verification_code=code
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_refresh_token(db, token):
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == token))
    return result.scalar_one_or_none()

async def create_refresh_token(db, token, user_id, expires_at):
    refresh_token = RefreshToken(token=token, user_id=user_id, expires_at=expires_at)
    db.add(refresh_token)
    await db.commit()
    await db.refresh(refresh_token)
    return refresh_token