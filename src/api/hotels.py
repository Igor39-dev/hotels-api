from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query, status
from fastapi.openapi.models import Example
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions import HotelNotFoundHTTPException, ObjectNotFoundException, check_date_to_after_date_from
from src.services.hotels import HotelService
from src.shemas.hotels import HotelAdd, SHotelPATCH

router = APIRouter(prefix="/hotels", tags=["ОТЕЛИ"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(default=None, description="Локация"),
    title: str | None = Query(default=None, description="Название отеля"),
    date_from: date = Query(openapi_examples={"пример": Example(value="2026-05-17")}),
    date_to: date = Query(openapi_examples={"пример": Example(value="2026-05-18")}),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Отель 4 seasons", "location": "Сочи,ул. Катина, 1"},
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Delux 1 звезда",
                    "location": "Дубай, ул. Шейха, 2",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await HotelService(db).partially_edit_hotel(hotel_id, hotel_data)
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
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
