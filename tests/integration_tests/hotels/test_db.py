from src.shemas.hotels import HotelAdd
from src.utlils.db_manager import DBManager
from src.database import async_session_maker_null_pool


async def test_add_hotel():
    hotel_data = HotelAdd(title="Test Hotel", location="Test Location")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        new_hotel_data = await db.hotels.add(hotel_data)
        await db.commit()

