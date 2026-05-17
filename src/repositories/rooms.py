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
        """
        select rooms_id, count(*) as rooms_booked from bookings
        where date_from <= '2026-05-17' and date_to >= '2026-05-17'
        group by rooms_id;
        """
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

        """
        rooms_left_table as (
            select rooms.id as room_id, rooms.quantity - coalesce(rooms_count.rooms_booked, 0) as rooms_left
            from rooms
            left join rooms_count on rooms.id = rooms_count.room_id
        )
        """
        rooms_left_table = (
            select(
                RoomsOrm.id.label("room_id"),
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )

        """
        select * from rooms_left_table
        where rooms_left > 0;
        """
        query = (
            select(rooms_left_table)
            .select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0)
        )

        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
