

class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"
