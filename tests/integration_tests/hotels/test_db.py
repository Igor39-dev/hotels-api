from src.shemas.hotels import HotelAdd
from src.utlils.db_manager import DBManager
from src.database import async_session_maker_null_pool


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Test Hotel", location="Test Location")
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()


async def test_add_hotel2(db):
    hotel_data = HotelAdd(title="Test Hotel 01", location="Test Location")
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()
