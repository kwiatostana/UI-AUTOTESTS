import allure

from pages.login_page import LoginPage
from src.constants import (ERROR_LOGIN_MESSAGE, INVALID_PASSWORD,
                           INVALID_USERNAME, SUCCESS_LOGIN_MESSAGE,
                           VALID_PASSWORD, VALID_USERNAME)


@allure.epic("Авторизация")
@allure.feature("Проверка авторизации")
@allure.story("Валидация входа и выхода пользователя")
@allure.severity(allure.severity_level.BLOCKER)
class TestLoginValidation:
    """Тест-кейс 4: Проверка авторизации"""

    @allure.title("Проверка отображения полей ввода и состояния кнопки Login")
    def test_login_input_fields_are_displayed(self, opened_login_page: LoginPage) -> None:
        with allure.step("Проверить отображение полей ввода"):
            assert opened_login_page.is_displayed(opened_login_page.USERNAME_FIELD), (
                "Поле ввода имени пользователя не отображается"
            )
            assert opened_login_page.is_displayed(opened_login_page.PASSWORD_FIELD), "Поле ввода пароля не отображается"

        with allure.step("Проверить состояние кнопки Login"):
            assert not opened_login_page.is_enabled(opened_login_page.LOGIN_BUTTON), (
                "Кнопка Login должна быть заблокирована до ввода данных"
            )

    @allure.title("Проверка успешной авторизации с валидными данными")
    def test_login_with_valid_credentials_succeeds(self, opened_login_page: LoginPage) -> None:
        opened_login_page.login(VALID_USERNAME, VALID_PASSWORD)

        with allure.step("Проверить сообщение об успешной авторизации"):
            success_message = opened_login_page.get_success_message()
            assert SUCCESS_LOGIN_MESSAGE in success_message, (
                f"Ожидалось сообщение '{SUCCESS_LOGIN_MESSAGE}', но получено '{success_message}'"
            )

    @allure.title("Проверка авторизации с невалидными данными")
    def test_login_with_invalid_credentials_fails(self, opened_login_page: LoginPage) -> None:
        opened_login_page.login(INVALID_USERNAME, INVALID_PASSWORD)

        with allure.step("Проверить сообщение об ошибке авторизации"):
            assert opened_login_page.get_error_message() == ERROR_LOGIN_MESSAGE

    @allure.title("Проверка успешного разлогирования")
    def test_logout_returns_to_login_form(self, opened_login_page: LoginPage) -> None:
        opened_login_page.login(VALID_USERNAME, VALID_PASSWORD)

        opened_login_page.logout()

        with allure.step("Проверить возврат к форме логина"):
            assert opened_login_page.is_displayed(opened_login_page.USERNAME_FIELD), (
                "Поле имени пользователя не отображается после разлогирования"
            )
            assert opened_login_page.is_displayed(opened_login_page.PASSWORD_FIELD), (
                "Поле пароля не отображается после разлогирования"
            )
