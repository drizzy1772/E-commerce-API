from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import CartItemCreate, CartResponse
from app.services.cart_service import add_to_cart
from app.services.auth_service import get_current_user
from app.models.models import User

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/items", response_model=CartResponse)
async def add_items(
    item:CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await add_to_cart(db, current_user.id, item.product_id, item.quantity)