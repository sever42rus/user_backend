class DoesNotExistException(Exception):
    def __init__(self, *args: object, message: str = "") -> None:
        self.message = message
        super().__init__(*args)


class MultipleObjectsException(Exception):
    def __init__(self, *args: object, message: str = "") -> None:
        self.message = message
        super().__init__(*args)


class BadRequestException(Exception):
    def __init__(self, *args: object, message: str = "") -> None:
        self.message = message
        super().__init__(*args)
