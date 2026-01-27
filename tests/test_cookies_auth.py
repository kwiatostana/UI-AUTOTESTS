import os

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.cookies_auth_page import CookiesAuthPage
from src.constants import COOKIE_FILE_PATH, COOKIES_LOGIN, COOKIES_PASSWORD


@allure.epic("Cookies")
@allure.feature("Auth with Cookies")
@allure.story("Авторизация с использованием Cookies")
@allure.severity(allure.severity_level.NORMAL)
@allure.id("TC_COOKIES_AUTH_001")
class TestCookiesAuth:
    """Тест-кейс 5: Авторизация с использованием Cookies"""

    @allure.title("Авторизация по логину и паролю, сохранение куков и авторизация уже по ним")
    def test_cookies_full_cycle(self, driver_class: WebDriver) -> None:
        page = CookiesAuthPage(driver_class)

        with allure.step("Выполнить первичный вход по логину и паролю"):
            page.open_page()
            page.login(COOKIES_LOGIN, COOKIES_PASSWORD)
            assert page.is_logged_in(), "Не удалось войти по логину и паролю"

        with allure.step("Сохранить куки в файл"):
            page.save_cookies_to_file(COOKIE_FILE_PATH)
            assert os.path.exists(COOKIE_FILE_PATH), "Файл с куками не был создан"

        with allure.step("Очистить куки для имитации закрытия браузера"):

            page.driver.delete_all_cookies()
            page.open_page()

            assert not page.is_logged_in(), "Пользователь должен быть разлогинен после тотальной очистки"

        with allure.step("Восстановить куки из файла и выполнить вход"):
            page.load_cookies_from_file(COOKIE_FILE_PATH)

        with allure.step("Проверить авторизацию после восстановления куков"):
            assert page.is_logged_in(), "Авторизация не восстановилась после загрузки куков"
