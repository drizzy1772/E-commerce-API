


from sqlalchemy import select
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import CartItemCreate, CartResponse
from app.services.cart_service import add_to_cart
from app.services.auth_service import get_current_user
from app.models.models import User, CartItem, Cart
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("")
async def get_cart_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        select(CartItem)
        .join(Cart)
        .where(Cart.user_id == current_user.id)
        .options(joinedload(CartItem.product))
    )
    result = await db.execute(query)
    order_items = result.scalars().all()


    for item in order_items:
        print(f"Item {item.product.name} | Price: {item.product.price}")

    response_data = []

    for item in order_items:
        cart_item_dict = {
            "id": item.id,
            "cart_id": item.cart_id,
            "product_id": item.product_id,
            "name": item.product.name,
            "quantity": item.quantity,
            "price": float(item.product.price)
        }

        response_data.append(cart_item_dict)

    return response_data



@router.post("/items", response_model=CartResponse)
async def add_items(
    item:CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await add_to_cart(db, current_user.id, item.product_id, item.quantity)