import allure

from pages.basic_auth_page import BasicAuthPage
from src.constants import BASIC_AUTH_LOGIN, BASIC_AUTH_PASSWORD


@allure.epic("Авторизация")
@allure.feature("Basic Auth")
@allure.story("Проверка базовой HTTP-авторизации")
@allure.severity(allure.severity_level.CRITICAL)
@allure.id("TC_BASIC_AUTH_001")
class TestBasicAuth:
    """Тест-кейс: Проверка Basic Auth авторизации"""

    @allure.title("Успешная авторизация Basic Auth")
    def test_basic_auth_success(self, opened_basic_auth_page: BasicAuthPage) -> None:
        with allure.step("Нажать кнопку отображения изображения"):
            opened_basic_auth_page.click_display_image()

        with allure.step("Пройти Basic Auth авторизацию"):
            opened_basic_auth_page.authenticate(BASIC_AUTH_LOGIN, BASIC_AUTH_PASSWORD)

        with allure.step("Проверить отображение секретного изображения"):
            assert opened_basic_auth_page.is_authenticated_image_displayed(), \
                "Секретное изображение не появилось после авторизации"
