










from app.config import settings
from app.routers import products, cart, orders, auth
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from app.exceptions import http_exception_handler, validation_exception_handler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from contextlib import asynccontextmanager
from redis import asyncio as aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_response=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    print("Redis was connected successfully")
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/api/docs/",
    lifespan=lifespan,
)


origins = [
    "http://localhost:3000",
    "http://localhost:5267",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(auth.router)


@app.get("/health/")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}


