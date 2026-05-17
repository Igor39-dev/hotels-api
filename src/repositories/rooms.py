from datetime import date
from sqlalchemy import select, func
from src.database import engine
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.models.bookings import BookingOrm
from src.shemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):

        rooms_count = (
            select(BookingOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingOrm)
            .filter(
                BookingOrm.date_from <= date_to,
                BookingOrm.date_to >= date_from,
            )
            .group_by(BookingOrm.room_id)
            .cte(name="rooms_count")
        )

        rooms_left_table = (
            select(
                RoomsOrm.id.label("room_id"),
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )

        rooms_ids_for_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery(name="rooms_ids_for_hotel")
        )
        
        rooms_ids_for_get = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotel),
                )
        )

        print(rooms_ids_for_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_for_get))
