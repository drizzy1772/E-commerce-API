






from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from app.models.models import Product, Cart, CartItem
from sqlalchemy import select

async def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int) -> CartItem:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    
    
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="product stock is more than quantity")
    
    result = await db.execute(select(Cart).where(Cart.user_id == user_id))
    cart = result.scalar_one_or_none()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        await db.commit()
        await db.refresh(cart)
    
    result = await db.execute(select(CartItem).where(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id,
    ))
    cart_item = result.scalar_one_or_none()
    
    
    if cart_item:
        
        cart_item.quantity += quantity
    
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.add(cart_item)
    
    await db.commit()
    await db.refresh(cart_item)
    return cart_item


