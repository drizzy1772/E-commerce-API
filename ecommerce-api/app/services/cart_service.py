






from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from app.models.models import Product, Cart, CartItem

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int) -> CartItem:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    
    
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="product stock is more than quantity")
    
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id,
    ).first()
    
    if cart_item:
        
        cart_item.quantity += quantity
    
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart_item)
    return cart_item


