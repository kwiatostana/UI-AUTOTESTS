import json
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from src.constants import COOKIE_FILE_PATH, COOKIES_URL


class CookiesAuthPage(BasePage):
    LOGIN_INPUT = (By.NAME, "login")
    PASSWORD_INPUT = (By.NAME, "psw")
    ENTER_BUTTON = (By.NAME, "subm1")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout.php']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = COOKIES_URL

    def open_page(self):
        self.open(self.url)
        return self

    def login(self, username, password):
        """Вход через форму"""
        self.send_keys(self.LOGIN_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.ENTER_BUTTON)
        return self

    def is_logged_in(self):
        """Проверка авторизации"""
        return self.is_present(self.LOGOUT_LINK)

    def logout(self):
        """Выход из системы"""
        self.click(self.LOGOUT_LINK)
        return self

    def save_cookies_to_file(self, file_path=COOKIE_FILE_PATH):
        """Запись куков в файл"""
        cookies = self.driver.get_cookies()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            json.dump(cookies, file, indent=4)

    def load_cookies_from_file(self, file_path=COOKIE_FILE_PATH):
        """Считывание куков из файла"""
        if not os.path.exists(file_path):
            return False

        with open(file_path) as file:
            cookies = json.load(file)

        self.open_page()

        self.driver.delete_all_cookies()

        for cookie in cookies:
            if "domain" in cookie:
                del cookie["domain"]

            if "expiry" in cookie:
                cookie["expiry"] = int(cookie["expiry"])

            if "secure" in cookie:
                cookie["secure"] = False

            self.driver.add_cookie(cookie)

        self.driver.refresh()
        return True
