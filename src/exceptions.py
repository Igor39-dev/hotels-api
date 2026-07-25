from datetime import date
from fastapi import HTTPException, status


class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Объект уже суЩествует"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
        if date_to <=date_from:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Дата заезда не может быть позже даты выезда")


class NabronirovalExceptionHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalExceptionHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(NabronirovalExceptionHTTPException):
    status_code = 404
    detail = "Номер не найден"
