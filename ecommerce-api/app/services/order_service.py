from app.models.models import Cart, CartItem, Order, OrderStatus, User, OrderItem
from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException
from app.services.email_service import send_order_status_email
from sqlalchemy import select

async def create_order(db: Session, user_id: int):
    result = await db.execute(select(Cart).where(Cart.user_id == user_id))
    cart = result.scalar_one_or_none()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    result = await db.execute(select(CartItem).where(CartItem.cart_id == cart.id).options(selectinload(CartItem.product)))
    cart_items = result.scalars().all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="card items was not founded")

    total_amount = 0
    for item in cart_items:
        total_amount += item.product.price * item.quantity
        
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
        db.delete(item)
    
    await db.commit()
    return order


async def get_order(db: Session, order_id: int):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="order was not founded")
    return order

async def update_order(db: Session, order_id: int, status: OrderStatus):
    result = await db.execute(select(Order).where(Order.id == order_id))
    
    order = result.scalar_one_or_none()
    
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