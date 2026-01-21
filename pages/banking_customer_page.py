import random
import re

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.banking_home_page import BankingHomePage
from pages.base_page import BasePage
from src.constants import ZERO


class BankingCustomerPage(BasePage):
    """Класс для работы со страницей Customer"""

    HOME_BUTTON = (By.CSS_SELECTOR, "button[ng-click='home()']")

    CUSTOMER_DROPDOWN = (By.CSS_SELECTOR, "#userSelect")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    WELCOME_MESSAGE = (By.CSS_SELECTOR, "span.ng-binding")

    DEPOSIT_BUTTON = (By.CSS_SELECTOR, "button[ng-click='deposit()']")
    WITHDRAWAL_BUTTON = (By.CSS_SELECTOR, "button[ng-click='withdrawl()']")
    TRANSACTIONS_BUTTON = (By.CSS_SELECTOR, "button[ng-click='transactions()']")

    AMOUNT_INPUT = (By.CSS_SELECTOR, "input[ng-model='amount']")
    DEPOSIT_SUBMIT = (By.CSS_SELECTOR, "button[value]")
    WITHDRAWAL_SUBMIT = (By.CSS_SELECTOR, "button[value]")

    DEPOSIT_SUCCESS_MESSAGE = (By.CSS_SELECTOR, "span[ng-show='message']")
    WITHDRAWAL_SUCCESS_MESSAGE = (By.CSS_SELECTOR, "span[ng-show='message']")
    WITHDRAWAL_FAILED_MESSAGE = (By.CSS_SELECTOR, "span[ng-show='message']")

    BALANCE_TEXT = (By.CSS_SELECTOR, "div[ng-hide='noAccount'] > strong:nth-child(2)")

    TRANSACTIONS_ROWS = (By.CSS_SELECTOR, "tr.ng-scope")
    TRANSACTION_BY_AMOUNT_XPATH = "//tr[contains(@class, 'ng-scope')]//td[text()='{amount}']"
    TRANSACTION_AMOUNT_CELL = (By.CSS_SELECTOR, "td:nth-child(2)")

    RESET_BUTTON = (By.CSS_SELECTOR, "button[ng-click='reset()']")
    BACK_BUTTON = (By.CSS_SELECTOR, "button[ng-click='back()']")

    @allure.step("Выбрать покупателя: {customer_name}")
    def select_customer(self, customer_name: str) -> "BankingCustomerPage":
        """Выбрать покупателя"""
        element = self.find_element(self.CUSTOMER_DROPDOWN)
        select = Select(element)
        select.select_by_visible_text(customer_name)
        return self

    @allure.step("Нажать кнопку Login")
    def click_login(self) -> "BankingCustomerPage":
        """Нажать кнопку Login"""
        self.click(self.LOGIN_BUTTON)
        return self

    @allure.step("Получить имя пользователя из приветственного сообщения")
    def get_name_in_welcome_message(self) -> str:
        """Получить имя пользователя из приветственного сообщения"""
        return self.find_element(self.WELCOME_MESSAGE).text

    @allure.step("Получить текущий баланс")
    def get_balance(self) -> int:
        """Получить текущий баланс"""
        balance_text = self.get_text(self.BALANCE_TEXT)
        numbers = re.findall(r"\d+", balance_text)
        if numbers:
            return int(numbers[0])
        raise ValueError(f"Не удалось извлечь баланс из текста: '{balance_text}'")

    @allure.step("Перейти в раздел Deposit")
    def click_deposit(self) -> "BankingCustomerPage":
        """Перейти в раздел Deposit"""
        self.click(self.DEPOSIT_BUTTON)
        return self

    @allure.step("Ввести сумму для депозита: {amount}")
    def enter_deposit_amount(self, amount: int) -> "BankingCustomerPage":
        """Ввести сумму для депозита"""
        self.send_keys(self.AMOUNT_INPUT, str(amount))
        return self

    @allure.step("Подтвердить внесение депозита")
    def submit_deposit(self) -> "BankingCustomerPage":
        """Подтвердить внесение депозита"""
        assert self.is_enabled(self.DEPOSIT_SUBMIT), "Кнопка Deposit заблокирована."
        self.click(self.DEPOSIT_SUBMIT)
        return self

    @allure.step("Получить сообщение об успешном депозите")
    def get_deposit_success_message(self) -> str:
        """Получить сообщение об успешном депозите"""
        return self.get_text(self.DEPOSIT_SUCCESS_MESSAGE)

    @allure.step("Перейти в раздел Withdrawal")
    def click_withdrawal(self) -> "BankingCustomerPage":
        """Перейти в раздел Withdrawal"""
        self.click(self.WITHDRAWAL_BUTTON)
        return self

    @allure.step("Ввести сумму для снятия: {amount}")
    def enter_withdrawal_amount(self, amount: int) -> "BankingCustomerPage":
        """Ввести сумму для снятия"""
        self.send_keys(self.AMOUNT_INPUT, str(amount))
        return self

    @allure.step("Подтвердить снятие средств")
    def submit_withdrawal(self) -> "BankingCustomerPage":
        """Подтвердить снятие средств"""
        self.click(self.WITHDRAWAL_SUBMIT)
        return self

    @allure.step("Получить сообщение о результате снятия средств")
    def get_withdrawal_message(self) -> str:
        """Получить сообщение о результате снятия средств"""
        return self.get_text(self.WITHDRAWAL_SUCCESS_MESSAGE)

    @allure.step("Перейти в раздел Transactions")
    def click_transactions(self) -> "BankingCustomerPage":
        """Перейти в раздел Transactions"""
        self.wait.until(EC.element_to_be_clickable(self.TRANSACTIONS_BUTTON))
        self.click(self.TRANSACTIONS_BUTTON)
        return self

    @allure.step("Получить количество транзакций")
    def get_transactions_count(self) -> int:
        """Получить количество транзакций"""
        transactions = self.find_elements(self.TRANSACTIONS_ROWS)
        return len(transactions)

    @allure.step("Подсчитать баланс из таблицы транзакций")
    def calculate_balance_from_transactions(self) -> int:
        """Подсчитать баланс из таблицы транзакций"""
        transactions = self.find_elements(self.TRANSACTIONS_ROWS)

        total_balance = ZERO
        for row in transactions:
            amount, trans_type = self._extract_data_from_transaction(row)
            if trans_type == "Credit":
                total_balance += amount
            elif trans_type == "Debit":
                total_balance -= amount

        return total_balance

    def _extract_data_from_transaction(self, transaction_row: WebElement) -> tuple[int, str]:
        """
        Извлечь данные из строки транзакции
        """
        cells = transaction_row.find_elements(By.TAG_NAME, "td")

        if not cells:
            return ZERO, ""

        amount_text = cells[1].text
        trans_type = cells[2].text

        return int(amount_text), trans_type

    def _extract_amount_from_transaction(self, transaction: WebElement) -> int:
        """Вспомогательный метод только для суммы (используется в is_transaction_present)"""
        amount, _ = self._extract_data_from_transaction(transaction)
        return amount

    @allure.step("Получить сумму последней транзакции")
    def get_last_transaction_amount(self) -> str:
        """Получить сумму последней транзакции"""
        self.wait.until(EC.presence_of_element_located(self.TRANSACTIONS_ROWS))
        transactions = self.find_elements(self.TRANSACTIONS_ROWS)
        return transactions[-1].find_element(*self.TRANSACTION_AMOUNT_CELL).text

    @allure.step("Проверить наличие транзакции с суммой {amount}")
    def is_transaction_present(self, amount: int) -> bool:
        """Проверить наличие транзакции с указанной суммой"""
        locator = (By.XPATH, self.TRANSACTION_BY_AMOUNT_XPATH.format(amount=amount))
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @allure.step("Сбросить список транзакций")
    def click_reset(self) -> "BankingCustomerPage":
        """Сбросить список транзакций"""
        self.click(self.RESET_BUTTON)
        return self

    @allure.step("Вернуться назад из раздела транзакций")
    def click_back(self) -> "BankingCustomerPage":
        """Вернуться назад из раздела транзакций"""
        self.click(self.BACK_BUTTON)
        return self

    @allure.step("Сгенерировать случайную сумму для снятия (макс {max_balance})")
    def get_random_withdrawal_amount(self, max_balance: int) -> int:
        """Сгенерировать случайную сумму для снятия в пределах баланса"""
        return random.randint(1, max_balance)

    @allure.step("Нажать кнопку Home")
    def click_home(self) -> "BankingCustomerPage":
        """Нажать кнопку Home для возврата на главную страницу"""
        self.click(self.HOME_BUTTON)
        return self

    @allure.step("Перейти в интерфейс Bank Manager Login через Home")
    def navigate_to_bank_manager_login_via_home(self) -> "BankingHomePage":
        """Перейти в интерфейс Bank Manager Login через Home страницу"""
        self.click_home()
        home_page = BankingHomePage(self.driver)
        home_page.navigate_to_bank_manager_login()
        return home_page
