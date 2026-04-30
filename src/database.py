import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.config import settings
from sqlalchemy import text


engine = create_async_engine(settings.DB_URL)

async def func():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT version()"))
        print(result.fetchone())

asyncio.run(func())
