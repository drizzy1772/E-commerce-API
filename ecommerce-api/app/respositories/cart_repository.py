



from sqlalchemy import select
from app.models.models import Product, Cart, CartItem

async def get_product_by_id(db, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()

async def get_cart_by_user_id(db, user_id: int):
    result = await db.execute(select(Cart).where(Cart.user_id == user_id))
    return result.scalar_one_or_none()

async def create_cart(db, user_id: int):
    cart = Cart(user_id=user_id)
    db.add(cart)
    await db.commit()
    await db.refresh(cart)
    
    return cart

async def get_cart_item(db, cart_id, product_id: int):
    result = await db.execute(select(CartItem).where(CartItem.cart_id == cart_id,
                                                     CartItem.product_id == product_id,))
    return result.scalar_one_or_none()

async def create_cart_item(db, cart_id, product_id, quantity):
    cartitem = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
    db.add(cartitem)
    await db.commit()
    await db.refresh(cartitem)
    return cartitem