from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import OrderResponse
from app.models.models import OrderStatus
from app.services.order_service import create_order, get_order, update_order
from app.services.auth_service import get_current_user
from app.models.models import User


router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
async def add_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = create_order(db, current_user.id)
    return order

@router.get("/{order_id}", response_model=OrderResponse)
async def getting_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = get_order(db, order_id)
    return order

@router.patch("/{order_id}/status", response_model=OrderResponse)
async def updating_order(
    status: OrderStatus,
    order_id: int,
    db: Session = Depends(get_db)
):
    update = update_order(db, order_id, status)
    return update