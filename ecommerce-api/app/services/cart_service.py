






from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from app.models.models import Product, Cart, CartItem
from sqlalchemy import select
from app.repositories import cart_repository

async def add_to_cart(db, user_id: int, product_id: int, quantity: int):
    product = await cart_repository.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    
    
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="product stock is more than quantity")
    
    cart = await cart_repository.get_cart_by_user_id(db, user_id)
    if not cart:
        cart = await cart_repository.create_cart(db, user_id)
    
    cart_item = await cart_repository.get_cart_item(db, cart.id, product_id)
    
    if cart_item:
        cart_item.quantity += quantity
        await db.commit()
        await db.refresh(cart_item)
    else:
        cart_item = await cart_repository.create_cart_item(db, cart.id, product_id, quantity)
    
    return cart_item


