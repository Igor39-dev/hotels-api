from src.repositories.base import BaseRepository
from src.models.bookings import BookingOrm
from src.shemas.bookings import Booking, BookingAdd



class BookingsRepository(BaseRepository):
    model = BookingOrm
    schema = Booking
