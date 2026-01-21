from collections.abc import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from pages.banking_home_page import BankingHomePage
from pages.banking_manager_page import BankingManagerPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from src.constants import BANKING_URL, HOME_URL, LOGIN_URL, POPUP_TIMEOUT
from utils.data_generator import (generate_customer_data,
                                  generate_registration_data)


@pytest.fixture
def driver() -> Generator[WebDriver]:
    """Фикстура для создания драйвера"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)

    yield driver

    driver.quit()


@pytest.fixture
def opened_home_page(driver: WebDriver) -> HomePage:
    """Фикстура для создания и открытия главной страницы"""
    page = HomePage(driver)
    page.open(HOME_URL)
    page.close_popup(wait_timeout=POPUP_TIMEOUT)
    return page


@pytest.fixture
def opened_login_page(driver: WebDriver) -> LoginPage:
    """Фикстура для создания и открытия страницы авторизации"""
    page = LoginPage(driver)
    page.open(LOGIN_URL)
    return page


@pytest.fixture(scope="class")
def driver_class() -> Generator[WebDriver]:
    """Фикстура драйвера с scope='class' для общего состояния во всех тестах класса"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)

    yield driver

    driver.quit()


@pytest.fixture(scope="class")
def banking_test_data_class(driver_class: WebDriver) -> Generator[dict[str, dict[str, str]]]:
    """Фикстура данных с scope='class'"""
    customer_data = generate_customer_data()
    registration_data = generate_registration_data()

    yield {"customer_data": customer_data, "registration_data": registration_data}

    try:
        home_page = BankingHomePage(driver_class)
        home_page.open(BANKING_URL)
        home_page.navigate_to_bank_manager_login()

        manager_page = BankingManagerPage(driver_class)
        manager_page.click_customers()
        manager_page.search_customer(customer_data["first_name"])
        customer_rows = manager_page.get_customer_row_texts()
        if any(customer_data["first_name"] in row for row in customer_rows):
            manager_page.delete_customer()
            manager_page.clear_search()
    except Exception as e:
        print(f"Ошибка при удалении клиента {customer_data['first_name']}: {e}")
