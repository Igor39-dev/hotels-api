import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend

logging.basicConfig(level=logging.DEBUG)

from src.api.auth import router as router_auth
from src.api.bookings import router as router_bookings
from src.api.dependencies import get_db
from src.api.facilities import router as router_facilities
from src.api.hotels import router as router_hotels
from src.api.images import router as router_images
from src.api.rooms import router as router_rooms
from src.config import settings
from src.init import redis_manager


async def send_emails_bookings_today_checkin():
    async for db in get_db():
        bookings = await db.bookings.get_bookings_with_today_checkin()
        # print(f"{bookings=}")


async def run_send_email_alltime():
    while True:
        await send_emails_bookings_today_checkin()
        await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(run_send_email_alltime())
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="cache")
    logging.info("FastAPI cache initialized")
    yield
    await redis_manager.close()


if settings.MODE == "TEST":
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

app = FastAPI(
    title="Hotels API",
    description="API для работы с отелями",
    lifespan=lifespan
)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(): ...


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8001, reload=True)
