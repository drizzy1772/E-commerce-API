




from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import OrderResponse
from app.models.models import OrderStatus
from app.services.order_service import create_order, get_order, update_order
from app.services.auth_service import get_current_user, require_admin
from app.models.models import User
from app.services.email_service import send_order_status_email

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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = get_order(db, order_id)
    return order

@router.patch("/{order_id}/status", response_model=OrderResponse)
async def updating_order(
    status: OrderStatus,
    order_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    update = update_order(db, order_id, status)
    user = db.query(User).filter(User.id == update.user_id).first()
    background_tasks.add_task(send_order_status_email, user.email, update.status, update.id)
    return update