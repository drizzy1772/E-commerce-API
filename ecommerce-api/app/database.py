



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
engine = create_async_engine(settings.DATABASE_URL.replace("postgresql://","postgresql+asyncpg://"))

asyncsession = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)



async def get_db():
    async with AsyncSession(engine) as session:
        yield session