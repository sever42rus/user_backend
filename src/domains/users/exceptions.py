class UniqueUserExceptions(Exception):
    """
    Исключение, вызываемое в случае, если пользователь с таким email уже существует.
    """

    pass


class UserLoginExceptions(Exception):
    """
    Исключение, вызываемое при неверных учетных данных пользователя при входе.
    """

    pass


class UserIsNoneExceptions(Exception):
    """
    Исключение, вызываемое в случае, если запрашиваемый пользователь не найден.
    """

    pass
