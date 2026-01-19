"""Page Object для страницы авторизации"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from src.constants import SUCCESS_LOGIN_MESSAGE


class LoginPage(BasePage):
    """Класс для работы со страницей авторизации"""

    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    USERNAME_DESCRIPTION_FIELD = (By.ID, "formly_1_input_username_0")  # не указана в тест-кейсе но она обязательна...
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".btn.btn-danger")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a[href='#/login']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div[ng-view]")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert.alert-danger")

    def enter_username(self, username: str) -> "LoginPage":
        """Ввести username в первое поле"""
        self.send_keys(self.USERNAME_FIELD, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Ввести password"""
        self.send_keys(self.PASSWORD_FIELD, password)
        return self

    def enter_username_description(self, username: str) -> "LoginPage":
        """Ввести username в обязательное поле description (второе поле username)"""
        self.send_keys(self.USERNAME_DESCRIPTION_FIELD, username)
        return self

    def submit_login(self) -> "LoginPage":
        """Нажать кнопку Login"""
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """Выполнить вход: заполняет все три поля (username, password, обязательное поле username)"""
        return (
            self.enter_username(username).enter_password(password).enter_username_description(username).submit_login()
        )

    def get_success_message(self) -> str:
        """Получить текст сообщения об успешной авторизации"""
        self.wait_for_text(self.SUCCESS_MESSAGE, SUCCESS_LOGIN_MESSAGE)
        return self.get_text(self.SUCCESS_MESSAGE)

    def get_error_message(self) -> str:
        """Получить текст сообщения об ошибке"""
        return self.get_text(self.ERROR_MESSAGE)

    def logout(self) -> "LoginPage":
        """Выполнить выход"""
        self.click(self.LOGOUT_BUTTON)
        return self
