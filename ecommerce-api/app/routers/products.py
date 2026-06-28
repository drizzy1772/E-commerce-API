



from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import ProductResponse
from app.services.product_service import get_products
from fastapi_cache.decorator import cache
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductResponse])
@cache(expire=60)
def read_items(
    search: str = None,
    category_id: int = None,
    min_price: float = None,
    max_price: float = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching products = {search}, category_id={category_id}, min_price={min_price}, max_price={max_price}")
    return get_products(db, search, category_id, min_price, max_price, skip, limit)






