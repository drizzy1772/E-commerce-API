










from app.config import settings
from app.routers import products, cart, orders, auth, health
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from app.exceptions import http_exception_handler, validation_exception_handler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import asyncio

from contextlib import asynccontextmanager
from redis import asyncio as aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_fastapi_instrumentator import Instrumentator
from app.services.events_consumer import order_status_listener

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_response=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    app.state.redis = redis

    listener_task = asyncio.create_task(order_status_listener(redis))


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


app.include_router(products.router, prefix="/api/v1")
app.include_router(cart.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(health.router)


Instrumentator().instrument(app).expose(app)


