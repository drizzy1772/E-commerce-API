







from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session
from app.models.models import Product, Cart, CartItem, Order, OrderItem, User



async def get_cart_items_with_product(db: Session, cart_id: int):
    products = (
        select(CartItem)
        .where(CartItem.cart_id == cart_id)
        .options(selectinload(CartItem.product))
    )
    result = await db.execute(products)
    return result.scalars().all()

async def create_order(db: Session, user_id: int, total_amount: float, status: str):
    new_order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status=status
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    
    return new_order

async def create_order_item(db: Session, order_id: int, product_id: int, quantity: int, unit_price: float):
    order_item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price
    )
    db.add(order_item)
    await db.commit()
    await db.refresh(order_item)
    
    return order_item

async def delete_cart_item(db: Session, cart_item: CartItem):
    db.delete(cart_item)
    await db.commit()

async def get_order_by_id(db: Session, order_id: int):
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()

async def get_user_by_id(db: Session, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()