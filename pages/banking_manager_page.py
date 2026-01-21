import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.banking_home_page import BankingHomePage
from pages.base_page import BasePage


class BankingManagerPage(BasePage):
    """Класс для работы со страницей Bank Manager"""

    HOME_BUTTON = (By.CSS_SELECTOR, "button[ng-click='home()']")

    ADD_CUSTOMER_BUTTON = (By.CSS_SELECTOR, "button[ng-click='addCust()']")
    OPEN_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[ng-click='openAccount()']")
    CUSTOMERS_BUTTON = (By.CSS_SELECTOR, "button[ng-click='showCust()']")

    FIRST_NAME_FIELD = (By.CSS_SELECTOR, "input[ng-model='fName']")
    LAST_NAME_FIELD = (By.CSS_SELECTOR, "input[ng-model='lName']")
    POST_CODE_FIELD = (By.CSS_SELECTOR, "input[ng-model='postCd']")
    ADD_CUSTOMER_BUTTON_SUBMIT = (By.CSS_SELECTOR, "button[type='submit'].btn.btn-default")

    CUSTOMER_DROPDOWN = (By.CSS_SELECTOR, "#userSelect")
    CURRENCY_DROPDOWN = (By.CSS_SELECTOR, "#currency")
    PROCESS_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')

    SEARCH_FIELD = (By.CSS_SELECTOR, "input.form-control")

    CUSTOMER_ROWS = (By.CSS_SELECTOR, "tr.ng-scope")

    DELETE_BUTTON = (By.CSS_SELECTOR, "button[ng-click='deleteCust(cust)']")

    @allure.step("Нажать кнопку Add Customer в меню")
    def click_add_customer(self) -> "BankingManagerPage":
        """Нажать кнопку Add Customer в меню"""
        self.click(self.ADD_CUSTOMER_BUTTON)
        return self

    @allure.step("Заполнить данные нового покупателя: {first_name} {last_name}, {post_code}")
    def fill_customer_data(self, first_name: str, last_name: str, post_code: str) -> "BankingManagerPage":
        """Заполнить данные нового покупателя"""
        return (
            self.send_keys(self.FIRST_NAME_FIELD, first_name)
            .send_keys(self.LAST_NAME_FIELD, last_name)
            .send_keys(self.POST_CODE_FIELD, post_code)
        )

    @allure.step("Нажать кнопку подтверждения добавления покупателя")
    def submit_add_customer(self) -> "BankingManagerPage":
        """Нажать кнопку подтверждения добавления покупателя"""
        self.click(self.ADD_CUSTOMER_BUTTON_SUBMIT)
        return self

    @allure.step("Принять уведомление об успешном добавлении покупателя")
    def accept_add_customer_alert(self) -> "BankingManagerPage":
        """Принять уведомление об успешном добавлении покупателя"""
        self.accept_alert()
        return self

    @allure.step("Нажать кнопку Open Account в меню")
    def click_open_account(self) -> "BankingManagerPage":
        """Нажать кнопку Open Account в меню"""
        self.click(self.OPEN_ACCOUNT_BUTTON)
        return self

    @allure.step("Получить текст всех опций в выпадающем списке покупателей")
    def get_customer_dropdown_options(self) -> list[str]:
        """Получить текст всех опций в выпадающем списке покупателей"""
        element = self.find_element(self.CUSTOMER_DROPDOWN)
        select = Select(element)
        return [option.text for option in select.options]

    @allure.step("Выбрать покупателя: {customer_name}")
    def select_customer(self, customer_name: str) -> "BankingManagerPage":
        """Выбрать покупателя из списка"""
        element = self.find_element(self.CUSTOMER_DROPDOWN)
        select = Select(element)
        select.select_by_visible_text(customer_name)
        return self

    @allure.step("Выбрать валюту: {currency}")
    def select_currency(self, currency: str) -> "BankingManagerPage":
        """Выбрать валюту"""
        element = self.find_element(self.CURRENCY_DROPDOWN)
        select = Select(element)
        select.select_by_visible_text(currency)
        return self

    @allure.step("Нажать кнопку Process для открытия счета")
    def click_process(self) -> "BankingManagerPage":
        """Нажать кнопку Process для открытия счета"""
        self.click(self.PROCESS_BUTTON)
        return self

    @allure.step("Принять уведомление об успешном открытии счета")
    def accept_open_account_alert(self) -> "BankingManagerPage":
        """Принять уведомление об успешном открытии счета"""
        self.accept_alert()
        return self

    @allure.step("Нажать кнопку Customers в меню")
    def click_customers(self) -> "BankingManagerPage":
        """Нажать кнопку Customers в меню"""
        self.click(self.CUSTOMERS_BUTTON)
        return self

    @allure.step("Найти покупателя по имени: {first_name}")
    def search_customer(self, first_name: str) -> "BankingManagerPage":
        """Найти покупателя по имени"""
        self.send_keys(self.SEARCH_FIELD, first_name)
        return self

    @allure.step("Получить текст всех строк в таблице покупателей")
    def get_customer_row_texts(self) -> list[str]:
        """Получить текст всех строк в таблице покупателей"""
        rows = self.find_elements(self.CUSTOMER_ROWS)
        return [row.text for row in rows]

    @allure.step("Удалить покупателя")
    def delete_customer(self) -> "BankingManagerPage":
        """Удалить покупателя"""

        self.click(self.DELETE_BUTTON)

        return self

    @allure.step("Очистить поле поиска")
    def clear_search(self) -> "BankingManagerPage":
        """Очистить поле поиска"""
        self.find_element(self.SEARCH_FIELD).clear()
        return self

    @allure.step("Нажать кнопку Home")
    def click_home(self) -> "BankingManagerPage":
        """Нажать кнопку Home для возврата на главную страницу"""
        self.click(self.HOME_BUTTON)
        return self

    @allure.step("Перейти в интерфейс Customer Login через Home")
    def navigate_to_customer_login_via_home(self) -> "BankingHomePage":
        """Перейти в интерфейс Customer Login через Home страницу"""
        self.click_home()
        home_page = BankingHomePage(self.driver)
        home_page.navigate_to_customer_login()
        return home_page
