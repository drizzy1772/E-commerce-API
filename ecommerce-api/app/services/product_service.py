


from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.models import Product





def get_products(db, search=None, category_id=None, min_price=None, max_price=None, skip=0, limit=20):
    query = select(Product)

    #it will find without a register, example: Phone, phone. Will find both
    if search:
        query = query.where(Product.name.ilike(f"%{search}%"))
    
    if category_id:
        query = query.where(Product.category_id == category_id)
    
    if min_price:
        query = query.where(Product.price >= min_price)
    
    if max_price:
        query = query.where(Product.price <= max_price)
    #it starts to do a skip of values that we dont need and it starts to make a limit on values.
    query = query.offset(skip).limit(limit)

    return db.execute(query).scalars().all()

