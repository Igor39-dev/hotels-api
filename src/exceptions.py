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

class EmailNotRegisteredException(NabronirovalException):
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordException(NabronirovalException):
    detail = "Пароль неверный"  


class UserAlreadyExistsException(NabronirovalException):
    detail = "Пользователь уже существует"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
        if date_to <=date_from:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Дата заезда не может быть позже даты выезда")


class NabronirovalHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = None

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Отель не найден"


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Номер не найден"
class EmailNotRegisteredHTTPException(NabronirovalHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordHTTPException(NabronirovalHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пароль неверный"


class UserEmailAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользоваетль с такой почтой уже существует"
