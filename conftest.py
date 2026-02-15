from collections.abc import Generator

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from driver_factory import DriverFactory
from pages.alerts_page import AlertsPage
from pages.banking_home_page import BankingHomePage
from pages.banking_manager_page import BankingManagerPage
from pages.basic_auth_page import BasicAuthPage
from pages.drag_n_drop_page import DragNDropPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.sample_form_page import SampleFormPage
from pages.tabs_page import TabsPage
from src.constants import (ALERTS_URL, BANKING_URL, BASIC_AUTH_URL,
                           DRAG_N_DROP_URL, HOME_URL, LOGIN_URL, POPUP_TIMEOUT,
                           SAMPLE_FORM_URL, TABS_URL)
from utils.data_generator import (generate_customer_data,
                                  generate_registration_data)


def pytest_addoption(parser):
    """Добавляем опции для выбора браузера и режима запуска"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "edge"],
        help="Браузер для тестов: chrome, firefox, edge"
    )
    parser.addoption(
        "--executor",
        action="store",
        default="local",
        choices=["local", "grid"],
        help="Режим запуска: локально или Selenium Grid"
    )
    parser.addoption(
        "--grid-url",
        action="store",
        default="http://localhost:4444",
        help="URL Selenium Grid (по умолчанию http://localhost:4444)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск браузера в headless-режиме"
    )


@pytest.fixture
def driver(request) -> Generator[WebDriver]:
    """Фикстура для создания драйвера через DriverFactory"""
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    grid_url = request.config.getoption("--grid-url")
    headless = request.config.getoption("--headless")

    driver = DriverFactory.create_driver(
        browser_name=browser,
        use_grid=(executor == "grid"),
        grid_url=grid_url,
        headless=headless
    )

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
def driver_class(request) -> Generator[WebDriver]:
    """Фикстура драйвера с scope='class' через DriverFactory"""
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    grid_url = request.config.getoption("--grid-url")
    headless = request.config.getoption("--headless")

    driver = DriverFactory.create_driver(
        browser_name=browser,
        use_grid=(executor == "grid"),
        grid_url=grid_url,
        headless=headless
    )

    yield driver

    driver.quit()


@pytest.fixture
def opened_drag_n_drop_page(driver: WebDriver) -> DragNDropPage:
    """Фикстура для создания и открытия страницы Drag and Drop"""
    page = DragNDropPage(driver)
    page.open(DRAG_N_DROP_URL)
    page.switch_to_demo_frame()
    return page


@pytest.fixture
def opened_tabs_page(driver: WebDriver) -> TabsPage:
    """Фикстура для создания и открытия страницы Tabs"""
    page = TabsPage(driver)
    page.open(TABS_URL)
    page.switch_to_demo_frame()
    return page


@pytest.fixture
def opened_alerts_page(driver: WebDriver) -> AlertsPage:
    """Фикстура для создания и открытия страницы Alerts"""
    page = AlertsPage(driver)
    page.open(ALERTS_URL)
    return page


@pytest.fixture
def opened_basic_auth_page(driver: WebDriver) -> BasicAuthPage:
    """Фикстура для создания и открытия страницы Basic Auth"""
    page = BasicAuthPage(driver)
    page.open(BASIC_AUTH_URL)
    return page


@pytest.fixture
def opened_sample_form_page(driver: WebDriver) -> SampleFormPage:
    """Фикстура для создания и открытия страницы Sample Form"""
    page = SampleFormPage(driver)
    page.open(SAMPLE_FORM_URL)
    return page


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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для получения результата выполнения теста"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request):
    """Автоматическое создание скриншота при падении теста"""
    yield

    if not (hasattr(request.node, "rep_call") and request.node.rep_call.failed):
        return

    driver = None
    if "driver" in request.fixturenames:
        driver = request.getfixturevalue("driver")
    elif "driver_class" in request.fixturenames:
        driver = request.getfixturevalue("driver_class")

    if driver:
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Не удалось создать скриншот: {e}")
