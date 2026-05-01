from pydantic import BaseModel, ConfigDict


class Hotel(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None
    