from src.shemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Test Hotel", location="Test Location")
    await db.hotels.add(hotel_data)
    await db.commit()


async def test_add_hotel2(db):
    hotel_data = HotelAdd(title="Test Hotel 01", location="Test Location")
    await db.hotels.add(hotel_data)
    await db.commit()
