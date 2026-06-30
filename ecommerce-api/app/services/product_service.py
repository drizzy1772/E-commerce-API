


from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.models import Product
from app.repositories import product_repository




async def get_products(db, search=None, category_id=None, min_price=None, max_price=None, skip=0, limit=20):
    query = select(Product)

    
    if search:
        query = query.where(Product.name.ilike(f"%{search}%"))
    
    if category_id:
        query = query.where(Product.category_id == category_id)
    
    if min_price:
        query = query.where(Product.price >= min_price)
    
    if max_price:
        query = query.where(Product.price <= max_price)
    
    query = query.offset(skip).limit(limit)

    return await product_repository.get_products(db, query)
