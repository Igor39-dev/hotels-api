from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.shemas.rooms import Room, RoomAdd


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(
        self,
        hotel_id: int
    ) -> list[Room]:
        query = select(RoomsOrm)
        query = query.filter(RoomsOrm.hotel_id == hotel_id)

        print(query.compile(compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        return [Room.model_validate(room, from_attributes=True) for room in result.scalars().all()]
