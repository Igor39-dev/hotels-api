from fastapi import Query, Body, APIRouter
from src.repositories.hotels import HotelsRepository
from src.api.dependencies import DBDep, PaginationDep
from src.database import async_session_maker
from src.shemas.hotels import Hotel, HotelAdd, SHotelPATCH


router = APIRouter(prefix="/hotels", tags=["ОТЕЛИ"])



@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(default=None, description="Локация"),
    title: str | None = Query(default=None, description="Название отеля"),
):
    per_page = pagination.per_page or 5

    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page-1)
    )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель 4 seasons",
            "location": "Сочи,ул. Катина, 1"
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Delux 1 звезда",
            "location": "Дубай, ул. Шейха, 2"
        }
    }
})):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}



@router.patch(
    "/{hotel_id}",
    summary="Чатичное удаление данных",
    description="<h1>Удаление данных отеля по ID, можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: SHotelPATCH,
):
    await db.hotels.edit(hotel_data, is_patch=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
