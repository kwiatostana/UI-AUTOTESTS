import uuid

from src.constants import POST_CODE_LENGTH


class DataGenerator:
    """Класс для генерации тестовых данных с использованием UUID"""

    @staticmethod
    def _get_unique_id() -> str:
        """Генерирует короткий уникальный идентификатор из UUID"""
        return str(uuid.uuid4())[:8].replace("-", "")

    @staticmethod
    def generate_first_name(unique_id: str | None = None) -> str:
        unique_id = unique_id or DataGenerator._get_unique_id()
        return f"TestUser{unique_id}"

    @staticmethod
    def generate_last_name(unique_id: str | None = None) -> str:
        unique_id = unique_id or DataGenerator._get_unique_id()
        return f"TestLastName{unique_id}"

    @staticmethod
    def generate_email(unique_id: str | None = None) -> str:
        unique_id = unique_id or DataGenerator._get_unique_id()
        return f"test{unique_id}@test.com"

    @staticmethod
    def generate_password(unique_id: str | None = None) -> str:
        unique_id = unique_id or DataGenerator._get_unique_id()
        return f"TestPass{unique_id}"

    @staticmethod
    def generate_post_code() -> str:
        """Генерирует почтовый индекс из 5 цифр UUID.int"""
        return f"{uuid.uuid4().int % (10**POST_CODE_LENGTH):0{POST_CODE_LENGTH}d}"

    @staticmethod
    def generate_customer_data(unique_id: str | None = None) -> dict[str, str]:
        unique_id = unique_id or DataGenerator._get_unique_id()
        return {
            "first_name": DataGenerator.generate_first_name(unique_id),
            "last_name": DataGenerator.generate_last_name(unique_id),
            "post_code": DataGenerator.generate_post_code(),
        }

    @staticmethod
    def generate_registration_data(unique_id: str | None = None) -> dict[str, str]:
        unique_id = unique_id or DataGenerator._get_unique_id()
        return {
            "first_name": DataGenerator.generate_first_name(unique_id),
            "last_name": DataGenerator.generate_last_name(unique_id),
            "email": DataGenerator.generate_email(unique_id),
            "password": DataGenerator.generate_password(unique_id),
        }
