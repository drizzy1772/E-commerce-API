




from fastapi import APIRouter, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import OrderResponse
from app.models.models import OrderStatus
from app.services.order_service import create_order, get_order, update_order
from app.services.auth_service import get_current_user, require_admin
from app.models.models import User
from app.services.email_service import send_order_status_email
from sqlalchemy import select
from fastapi.responses import JSONResponse
from app.dependencies.idempotency import check_idempotency_key
from app.models.enums import IdempotencyStatus
from app.services.events import publish_order_status_changed
from typing import List
from app.models.models import Order

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse, status_code=201)
async def add_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    idempotency_record = Depends(check_idempotency_key),
):  
    
    if isinstance(idempotency_record, JSONResponse):
        return idempotency_record
    order = await create_order(db, current_user.id)

    idempotency_record.status = IdempotencyStatus.COMPLETED
    idempotency_record.response_status = 201
    idempotency_record.response_body = OrderResponse.model_validate(order).model_dump(mode="json")

    await db.commit()

    return order


@router.get("", response_model=List[OrderResponse])
async def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = select(Order).where(Order.user_id == current_user.id)

    result = await db.execute(stmt)

    items = result.scalars().all()

    return items

@router.get("/{order_id}", response_model=OrderResponse)
async def getting_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = await get_order(db, order_id)
    return order

@router.patch("/{order_id}/status", response_model=OrderResponse)
async def updating_order(
    status: OrderStatus,
    order_id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    update = await update_order(db, order_id, status)
    result = await db.execute(select(User).where(User.id == update.user_id))
    user = result.scalar_one_or_none()
    background_tasks.add_task(send_order_status_email, user.email, update.status, update.id)

    background_tasks.add_task(publish_order_status_changed, request.app.state.redis, update.id, update.status)

    return update
