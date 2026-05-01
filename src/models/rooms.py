from cgi import print_exception
from turtle import title
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, String

from src.database import Base


class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(Integer, ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]