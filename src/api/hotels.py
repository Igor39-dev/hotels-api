from typing import Annotated
from fastapi import Query, Body, APIRouter, Depends
from src.api.dependencies import PaginationDep
from src.shemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["ОТЕЛИ"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубау", "name": "dubai"},
    {"id": 3, "title": "Москва", "name": "moscow"}, 
    {"id": 4, "title": "Санкт-Петербург", "name": "spb"},
    {"id": 5, "title": "Екатеринбург", "name": "ekb"},
    {"id": 6, "title": "Новосибирск", "name": "nsk"},
    {"id": 7, "title": "Красноярск", "name": "krasnoyarsk"},
    {"id": 8, "title": "Хабаровск", "name": "habarovsk"},
    {"id": 9, "title": "Владивосток", "name": "vladivostok"},
    {"id": 10, "title": "Магадан", "name": "magadan"},
    {"id": 11, "title": "Иркутск", "name": "irkutsk"},
]


@router.get("")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(default=None, description="ID отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]
    return hotels_

@router.post("")
def create_hotel(hotel: Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel.title,
        "name": hotel.name,
    })
    return {"status": "OK"}


@router.put("/{hotel_id}")
def edit_hotel(
    hotel_id: int,
    title: str = Body(),
    name: str = Body(),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["name"] = name
    return {"status": "OK"}



@router.patch(
    "/{hotel_id}",
    summary="Чатичное удаление данных",
    description="<h1>Удаление данных отеля по ID, можно отправить name, а можно title</h1>",
)
def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}