import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class BankingHomePage(BasePage):
    """Класс для работы с главной страницей Banking"""

    SAMPLE_FORM_BUTTON = (By.CSS_SELECTOR, "a[href*='registrationform.html']")
    BANK_MANAGER_LOGIN_BUTTON = (By.CSS_SELECTOR, "button[ng-click='manager()']")
    CUSTOMER_LOGIN_BUTTON = (By.CSS_SELECTOR, "button[ng-click='customer()']")

    @allure.step("Перейти в интерфейс Sample Form")
    def navigate_to_sample_form(self) -> "BankingHomePage":
        """Перейти в интерфейс Sample Form"""
        self.click(self.SAMPLE_FORM_BUTTON)
        return self

    @allure.step("Перейти в интерфейс Bank Manager Login")
    def navigate_to_bank_manager_login(self) -> "BankingHomePage":
        """Перейти в интерфейс Bank Manager Login"""
        self.click(self.BANK_MANAGER_LOGIN_BUTTON)
        return self

    @allure.step("Перейти в интерфейс Customer Login")
    def navigate_to_customer_login(self) -> "BankingHomePage":
        """Перейти в интерфейс Customer Login"""
        self.click(self.CUSTOMER_LOGIN_BUTTON)
        return self
