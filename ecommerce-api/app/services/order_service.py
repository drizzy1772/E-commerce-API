from app.models.models import Cart, CartItem, Order, OrderStatus, User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.email_service import send_order_status_email


def create_order(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
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
    db.commit()
    db.refresh(order)
    
    for item in cart_items:
        db.delete(item)
    db.commit()
    return order

def get_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="order was not founded")
    return order

def update_order(db: Session, order_id: int, status: OrderStatus):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="order was not found")
    user = db.query(User).filter(User.id == order.user_id).first()
    order.status = status
    db.commit()
    db.refresh(order)
    send_order_status_email(user.email, order.id, order.status)
    return order