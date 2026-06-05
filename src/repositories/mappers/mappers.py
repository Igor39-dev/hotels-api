from src.repositories.mappers.base import DataMapper
from src.models.hotels import HotelsOrm
from src.shemas.hotels import Hotel
from src.models.rooms import RoomsOrm
from src.shemas.rooms import Room, RoomWtihRels
from src.models.users import UsersOrm
from src.shemas.users import User
from src.models.bookings import BookingOrm
from src.shemas.bookings import Booking
from src.models.facilities import FacilitiesOrm
from src.shemas.facilities import Facility


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWtihRels

class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingOrm
    schema = Booking


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility
