"""
Демонстрационные тесты с намеренными падениями для проверки скриншотов в Allure.
"""

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.banking_home_page import BankingHomePage
from pages.banking_manager_page import BankingManagerPage
from pages.sample_form_page import SampleFormPage
from src.constants import (BANKING_URL, GENDER_FEMALE,
                           REGISTRATION_SUCCESS_MESSAGE, SAMPLE_FORM_URL)


@allure.epic("Демонстрационные падающие тесты")
@allure.feature("Скриншоты при падении")
@allure.story("Негативные сценарии для демонстрации")
@allure.severity(allure.severity_level.NORMAL)
@allure.id("TC_DEMO_FAIL_001")
class TestDemoFailures:
    """Демонстрационные тесты с некорректными данными для проверки скриншотов"""

    @allure.title("Регистрация с некорректным email")
    def test_registration_with_invalid_email(self, driver_class: WebDriver) -> None:
        sample_form_page = SampleFormPage(driver_class)
        sample_form_page.open(SAMPLE_FORM_URL)

        with allure.step("Заполнить форму с некорректным email"):
            sample_form_page.fill_registration_form(
                "Jone",
                "Doe",
                "not-a-valid-email",
                "Password123!",
            ).select_hobby().send_keys(sample_form_page.ABOUT_YOURSELF_FIELD, "About myself").select_gender(GENDER_FEMALE).submit_registration()

        with allure.step("Проверить сообщение об успешной регистрации"):
            assert sample_form_page.wait_for_text(
                sample_form_page.SUCCESS_MESSAGE, REGISTRATION_SUCCESS_MESSAGE
            ), f"Сообщение '{REGISTRATION_SUCCESS_MESSAGE}' не появилось"

    @allure.title("Добавление покупателя с пустыми полями")
    def test_add_customer_with_empty_fields(self, driver_class: WebDriver) -> None:
        home_page = BankingHomePage(driver_class)
        home_page.open(BANKING_URL)
        home_page.navigate_to_bank_manager_login()

        manager_page = BankingManagerPage(driver_class)
        manager_page.click_add_customer()

        with allure.step("Отправить форму с пустыми полями"):
            manager_page.fill_customer_data("", "", "").submit_add_customer()

        with allure.step("Проверить появление alert с подтверждением"):
            assert manager_page.wait_for_alert() is not None, "Alert не появился"
            manager_page.accept_add_customer_alert()
