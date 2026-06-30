from app.models.models import Cart, CartItem, Order, OrderStatus, User, OrderItem
from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException
from app.services.email_service import send_order_status_email
from sqlalchemy import select
from app.repositories import order_repository, cart_repository


async def create_order(db: Session, user_id: int):
    cart = await cart_repository.get_cart_by_user_id(db, user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart_items = await order_repository.get_cart_items_with_product(db, cart.id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="card items was not founded")

    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    
    
    
    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="pending"
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.product.price
            
        )
        db.add(order_item)
        await db.delete(item)
    
    await db.commit()
    return order


async def get_order(db: Session, order_id: int):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="order was not founded")
    return order

async def update_order(db: Session, order_id: int, status: OrderStatus):
    order = await order_repository.get_order_by_id(db, order_id)

    
    if not order:
        raise HTTPException(status_code=404, detail="order was not found")

    if order.status in [OrderStatus.cancelled, OrderStatus.delivered]:
        raise HTTPException(
            status_code=400,
            detail="Cannot update a cancelled order or delivered "
        )
    
    order.status = status
    await db.commit()
    await db.refresh(order)
    return order