from src.repositories.base import BaseRepository
from src.models.bookings import BookingOrm
from src.shemas.bookings import Booking, BookingAdd
from src.repositories.mappers.mappers import BookingDataMapper



class BookingsRepository(BaseRepository):
    model = BookingOrm
    mapper = BookingDataMapper()
