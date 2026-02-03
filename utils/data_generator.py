from faker import Faker

from src.constants import POST_CODE_LENGTH

_fake = Faker()


def generate_customer_data() -> dict[str, str]:
    """Генерирует данные для создания клиента"""
    return {
        "first_name": _fake.first_name(),
        "last_name": _fake.last_name(),
        "post_code": _fake.postcode()[:POST_CODE_LENGTH],
    }


def generate_registration_data() -> dict[str, str]:
    """Генерирует данные для регистрации пользователя"""
    return {
        "first_name": _fake.first_name(),
        "last_name": _fake.last_name(),
        "email": _fake.email(),
        "password": _fake.password(),
    }


def generate_random_name() -> str:
    """Генерирует случайное имя"""
    return _fake.first_name()
