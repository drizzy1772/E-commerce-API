


from fastapi import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import ProductResponse, PaginatedResponse
from app.services.product_service import get_products
from fastapi_cache.decorator import cache
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=PaginatedResponse[ProductResponse])
@cache(expire=60)
async def read_items(
    search: str = None,
    category_id: int = None,
    min_price: float = None,
    max_price: float = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="min_price cannot be greater than max_price")
    logger.info(f"Fetching products = {search}, category_id={category_id}, min_price={min_price}, max_price={max_price}")

    items, total = await get_products(db, search, category_id, min_price, max_price, skip, limit)
    has_next = skip + limit < total

    return PaginatedResponse(
        items=[ProductResponse.model_validate(item) for item in items],
        total=total,
        has_next=has_next
    )




