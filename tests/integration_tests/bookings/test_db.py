from datetime import date
from src.shemas.bookings import BookingAdd


async def test_add_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=8, day=10),
        date_to=date(year=2026, month=8, day=20),
        price=100
    )
    new_booking = await db.bookings.add(booking_data)

    # получить эту бронь и убедиться что она есть в базе данных
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking is not None
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    # обновить бронь
    updated_date = date(year=2026, month=8, day=25)
    updated_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=8, day=10),
        date_to=updated_date,
        price=100
    )
    await db.bookings.edit(updated_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == updated_date

    # удалить бронь
    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
