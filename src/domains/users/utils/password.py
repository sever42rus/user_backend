import base64
import hashlib
import os


def hash_password(password: str, hash_name: str = "sha256", iterations: int = 100000) -> str:
    """
    Хэширует пароль с использованием PBKDF2 и возвращает хэш в формате строки.

    :param password: Пароль пользователя
    :return: Хэшированный пароль в виде строки
    """
    salt = os.urandom(32)
    # Хэширование пароля
    dk = hashlib.pbkdf2_hmac(
        hash_name=hash_name,  # Используем SHA-256
        password=password.encode(),  # Кодируем пароль в байты
        salt=salt,  # Соль
        iterations=iterations,  # Количество итераций
    )

    # Форматируем хэш как строку
    hashed_password = base64.b64encode(salt + dk).decode("ascii")
    return f"{hash_name}::{iterations}::{hashed_password}"


def verify_password(stored_password: str, provided_password: str) -> bool:
    """
    Проверяет, совпадает ли предоставленный пароль с хэшированным паролем.

    :param stored_password: Хэшированный пароль из базы данных
    :param provided_password: Предоставленный пароль для проверки
    :return: True если пароли совпадают, иначе False
    """
    try:
        hash_name, iterations, stored_password = stored_password.split("::")
        decoded = base64.b64decode(stored_password)
        salt = decoded[:32]
        stored_hash = decoded[32:]

        # Хэшируем предоставленный пароль с тем же солью
        dk = hashlib.pbkdf2_hmac(
            hash_name=hash_name,
            password=provided_password.encode(),
            salt=salt,
            iterations=int(iterations),
        )

        return dk == stored_hash
    except Exception as e:
        print(f"Error during password verification: {e}")
        return False
