import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.banking_customer_page import BankingCustomerPage
from pages.banking_home_page import BankingHomePage
from pages.banking_manager_page import BankingManagerPage
from pages.sample_form_page import SampleFormPage
from src.constants import (BANKING_URL, DEPOSIT_AMOUNT,
                           DEPOSIT_SUCCESS_MESSAGE, GENDER_FEMALE,
                           REGISTRATION_SUCCESS_MESSAGE, SAMPLE_FORM_URL,
                           WITHDRAWAL_AMOUNT_LARGE, WITHDRAWAL_FAILED_MESSAGE,
                           WITHDRAWAL_SUCCESS_MESSAGE, ZERO)


@allure.feature("Тесты банковского приложения")
class TestBankingE2E:
    """Тест-кейс 5: Банковское приложение"""

    @allure.title("5.1 Регистрация в Sample Form")
    def test_registration_in_sample_form(
        self, driver_class: WebDriver, banking_test_data_class: dict[str, dict[str, str]]
    ) -> None:
        registration_data = banking_test_data_class["registration_data"]

        sample_form_page = SampleFormPage(driver_class)
        sample_form_page.open(SAMPLE_FORM_URL)

        with allure.step("Найти самое длинное слово из хобби"):
            hobby_words = sample_form_page.get_hobby_words()
            assert hobby_words, "Не удалось найти хобби. Проверьте локатор HOBBIES_LABELS."
            longest_word = max(hobby_words, key=len)

        with allure.step("Заполнить форму регистрации и отправить"):
            about_text = f"Самое длинное слово из предложенных хобби - {longest_word}"
            sample_form_page.fill_registration_form(
                registration_data["first_name"],
                registration_data["last_name"],
                registration_data["email"],
                registration_data["password"],
            ).select_hobby().send_keys(sample_form_page.ABOUT_YOURSELF_FIELD, about_text).select_gender(
                GENDER_FEMALE
            ).submit_registration()

        with allure.step("Проверить сообщение об успешной регистрации"):
            assert sample_form_page.wait_for_text(sample_form_page.SUCCESS_MESSAGE, REGISTRATION_SUCCESS_MESSAGE), (
                f"Сообщение об успешной регистрации '{REGISTRATION_SUCCESS_MESSAGE}' не появилось"
            )

    @allure.title("5.2.1 Добавление покупателя")
    def test_add_customer(self, driver_class: WebDriver, banking_test_data_class: dict[str, dict[str, str]]) -> None:
        customer_data = banking_test_data_class["customer_data"]

        home_page = BankingHomePage(driver_class)
        home_page.open(BANKING_URL)

        with allure.step("Перейти в интерфейс Bank Manager Login"):
            home_page.navigate_to_bank_manager_login()

        manager_page = BankingManagerPage(driver_class)

        with allure.step("Нажать Add Customer"):
            manager_page.click_add_customer()

        with allure.step("Заполнить данные покупателя и добавить"):
            manager_page.fill_customer_data(
                customer_data["first_name"], customer_data["last_name"], customer_data["post_code"]
            ).submit_add_customer()

        with allure.step("Проверить появление всплывающего окна с подтверждением"):
            assert manager_page.wait_for_alert() is not None, "Окно подтверждения (alert) не появилось"
            manager_page.accept_add_customer_alert()

    @allure.title("5.2.2 Открытие аккаунта")
    def test_open_account(self, driver_class: WebDriver, banking_test_data_class: dict[str, dict[str, str]]) -> None:
        customer_data = banking_test_data_class["customer_data"]
        customer_full_name = f"{customer_data['first_name']} {customer_data['last_name']}"

        home_page = BankingHomePage(driver_class)
        home_page.open(BANKING_URL)

        with allure.step("Перейти в интерфейс Bank Manager Login"):
            home_page.navigate_to_bank_manager_login()

        manager_page = BankingManagerPage(driver_class)
        manager_page.click_open_account()

        with allure.step("Проверить наличие клиента в выпадающем списке"):
            assert customer_full_name in manager_page.get_customer_dropdown_options(), (
                f"Клиент {customer_full_name} не найден в выпадающем списке после создания"
            )

        with allure.step("Выбрать клиента, валюту и обработать"):
            manager_page.select_customer(customer_full_name).select_currency("Dollar").click_process()

        with allure.step("Проверить появление всплывающего окна с подтверждением"):
            assert manager_page.wait_for_alert() is not None, "Окно подтверждения (alert) не появилось"
            manager_page.accept_open_account_alert()

    @allure.title("5.3 Вход в Customer Login и проверка приветствия")
    def test_customer_login_and_welcome(
        self, driver_class: WebDriver, banking_test_data_class: dict[str, dict[str, str]]
    ) -> None:
        customer_data = banking_test_data_class["customer_data"]
        customer_full_name = f"{customer_data['first_name']} {customer_data['last_name']}"

        manager_page = BankingManagerPage(driver_class)
        manager_page.navigate_to_customer_login_via_home()

        customer_page = BankingCustomerPage(driver_class)

        with allure.step("Выбрать созданного покупателя"):
            customer_page.select_customer(customer_full_name)

        with allure.step("Нажать Login"):
            customer_page.click_login()

        with allure.step("Убедиться, что вошли в нужный аккаунт и на экране есть приветствие"):
            expected_name = f"{customer_data['first_name']} {customer_data['last_name']}"
            welcome_name = customer_page.get_name_in_welcome_message().strip()
            assert welcome_name == expected_name, (
                f"Имя в приветствии '{welcome_name}' не совпадает с ожидаемым '{expected_name}'"
            )

    @allure.title("5.3.1 Успешное пополнение счета")
    def test_successful_deposit(
        self, driver_class: WebDriver, banking_test_data_class: dict[str, dict[str, str]]
    ) -> None:
        customer_data = banking_test_data_class["customer_data"]
        customer_full_name = f"{customer_data['first_name']} {customer_data['last_name']}"

        customer_page = BankingCustomerPage(driver_class)
        customer_page.click_home()
        home_page = BankingHomePage(driver_class)
        home_page.navigate_to_customer_login()
        customer_page.select_customer(customer_full_name).click_login()

        with allure.step("Нажать кнопку Deposit"):
            customer_page.click_deposit()

        with allure.step("Ввести сумму 100321"):
            customer_page.enter_deposit_amount(DEPOSIT_AMOUNT)

        with allure.step("Нажать на кнопку подтверждения Deposit"):
            customer_page.submit_deposit()

        with allure.step("Проверить появления сообщения Deposit Successful"):
            assert customer_page.get_deposit_success_message() == DEPOSIT_SUCCESS_MESSAGE, (
                "Сообщение об успешном пополнении счета не отображается или содержит неверный текст"
            )

        with allure.step("Перейти в Transactions"):
            customer_page.click_transactions()

        with allure.step("Проверить наличие пополнения на 100321"):
            assert str(DEPOSIT_AMOUNT) == customer_page.get_last_transaction_amount(), (
                f"Сумма последней транзакции не совпадает с суммой пополнения {DEPOSIT_AMOUNT}"
            )
            customer_page.click_back()

    @allure.title("5.3.2 Неуспешное пополнение счета")
    def test_unsuccessful_deposit(
        self, driver_class: WebDriver, banking_test_data_class: dict[str, dict[str, str]]
    ) -> None:
        customer_data = banking_test_data_class["customer_data"]
        customer_full_name = f"{customer_data['first_name']} {customer_data['last_name']}"

        customer_page = BankingCustomerPage(driver_class)
        customer_page.click_home()
        home_page = BankingHomePage(driver_class)
        home_page.navigate_to_customer_login()
        customer_page.select_customer(customer_full_name).click_login()

        with allure.step("Нажать кнопку Deposit"):
            customer_page.click_deposit()

        with allure.step("Ввести сумму 0"):
            customer_page.enter_deposit_amount(ZERO)

        with allure.step("Нажать на кнопку подтверждения Deposit"):
            customer_page.submit_deposit()

        with allure.step("Проверить отсутствие сообщения Deposit Successful"):
            assert not customer_page.wait_for_text(customer_page.DEPOSIT_SUCCESS_MESSAGE, DEPOSIT_SUCCESS_MESSAGE), (
                "Сообщение об успешном пополнении появилось при пополнении на 0"
            )

        with allure.step("Перейти в Transactions"):
            customer_page.click_transactions()

        with allure.step("Проверить отсутствие пополнения на 0"):
            assert str(ZERO) != customer_page.get_last_transaction_amount(), (
                "Транзакция на сумму 0 была ошибочно создана"
            )
            customer_page.click_back()

    @allure.title("5.3.3 Успешное снятие средств")
    def test_successful_withdrawal(
        self, driver_class: WebDriver, banking_test_data_class: dict[str, dict[str, str]]
    ) -> None:
        customer_data = banking_test_data_class["customer_data"]
        customer_full_name = f"{customer_data['first_name']} {customer_data['last_name']}"

        customer_page = BankingCustomerPage(driver_class)
        customer_page.click_home()
        home_page = BankingHomePage(driver_class)
        home_page.navigate_to_customer_login()
        customer_page.select_customer(customer_full_name).click_login()

        with allure.step("Получить состояние баланса счета"):
            balance = customer_page.get_balance()
            withdrawal_amount = customer_page.get_random_withdrawal_amount(balance)

        with allure.step("Нажать кнопку Withdrawn"):
            customer_page.click_withdrawal()

        with allure.step("Ввести рандомную сумму N (от 1 до максимума на балансе)"):
            customer_page.enter_withdrawal_amount(withdrawal_amount)

        with allure.step("Нажать на кнопку подтверждения Withdrawn"):
            customer_page.submit_withdrawal()

        with allure.step("Проверить наличие сообщения Transaction successful"):
            assert customer_page.get_withdrawal_message() == WITHDRAWAL_SUCCESS_MESSAGE, (
                "Сообщение об успешном снятии средств не отображается или неверно"
            )

        with allure.step("Перейти в Transactions"):
            customer_page.click_transactions()

        with allure.step("Проверить наличие снятия средств на сумму N"):
            assert customer_page.is_transaction_present(withdrawal_amount), (
                f"Транзакция на сумму {withdrawal_amount} не найдена"
            )
            customer_page.click_back()

    @allure.title("5.3.4 Неуспешное снятие средств")
    def test_unsuccessful_withdrawal(
        self, driver_class: WebDriver, banking_test_data_class: dict[str, dict[str, str]]
    ) -> None:
        customer_data = banking_test_data_class["customer_data"]
        customer_full_name = f"{customer_data['first_name']} {customer_data['last_name']}"

        customer_page = BankingCustomerPage(driver_class)
        customer_page.click_home()
        home_page = BankingHomePage(driver_class)
        home_page.navigate_to_customer_login()
        customer_page.select_customer(customer_full_name).click_login()

        with allure.step("Нажать кнопку Withdrawn"):
            customer_page.click_withdrawal()

        with allure.step("Ввести сумму 1000000"):
            customer_page.enter_withdrawal_amount(WITHDRAWAL_AMOUNT_LARGE)

        with allure.step("Нажать на кнопку подтверждения Withdrawn"):
            customer_page.submit_withdrawal()

        with allure.step("Проверить наличие сообщения об ошибке"):
            assert customer_page.get_withdrawal_message() == WITHDRAWAL_FAILED_MESSAGE, (
                "Сообщение о неудачном снятии средств (из-за нехватки баланса) не отображается или неверно"
            )

        with allure.step("Перейти в Transactions"):
            customer_page.click_transactions()

        with allure.step("Проверить отсутствие снятия средств на 1000000"):
            assert not customer_page.is_transaction_present(WITHDRAWAL_AMOUNT_LARGE), (
                f"Транзакция на сумму {WITHDRAWAL_AMOUNT_LARGE} была ошибочно создана при нехватке баланса"
            )
            customer_page.click_back()

    @allure.title("5.3.5 Проверка баланса")
    def test_balance_verification(
        self, driver_class: WebDriver, banking_test_data_class: dict[str, dict[str, str]]
    ) -> None:
        customer_data = banking_test_data_class["customer_data"]
        customer_full_name = f"{customer_data['first_name']} {customer_data['last_name']}"

        customer_page = BankingCustomerPage(driver_class)
        customer_page.click_home()
        home_page = BankingHomePage(driver_class)
        home_page.navigate_to_customer_login()
        customer_page.select_customer(customer_full_name).click_login()

        with allure.step("Получить состояние баланса счета"):
            balance = customer_page.get_balance()

        with allure.step("Нажать кнопку Transactions"):
            customer_page.click_transactions()

        with allure.step("Сделать подсчет баланса из таблицы"):
            calculated_balance = customer_page.calculate_balance_from_transactions()

        with allure.step("Проверить, что данные сходятся"):
            assert balance == calculated_balance, f"Баланс не сходится: {balance} != {calculated_balance}"
            customer_page.click_back()

    @allure.title("5.3.6 Снятие оставшихся средств")
    def test_withdraw_all_remaining_funds(
        self, driver_class: WebDriver, banking_test_data_class: dict[str, dict[str, str]]
    ) -> None:
        customer_data = banking_test_data_class["customer_data"]
        customer_full_name = f"{customer_data['first_name']} {customer_data['last_name']}"

        customer_page = BankingCustomerPage(driver_class)
        customer_page.click_home()
        home_page = BankingHomePage(driver_class)
        home_page.navigate_to_customer_login()
        customer_page.select_customer(customer_full_name).click_login()

        with allure.step("Получить состояние баланса счета"):
            balance = customer_page.get_balance()

        with allure.step("Нажать кнопку Withdrawn"):
            customer_page.click_withdrawal()

        with allure.step("Ввести сумму, оставшуюся на счету"):
            customer_page.enter_withdrawal_amount(balance)

        with allure.step("Нажать на кнопку подтверждения Withdrawn"):
            customer_page.submit_withdrawal()

        with allure.step("Проверить наличие сообщения Transaction successful"):
            assert customer_page.get_withdrawal_message() == WITHDRAWAL_SUCCESS_MESSAGE, (
                "Сообщение об успешном снятии средств не отображается или неверно"
            )

        with allure.step("Проверить, что отображается Balance : 0"):
            assert customer_page.get_balance() == ZERO, f"Баланс не равен {ZERO} после снятия всех средств"

    @allure.title("5.3.7 Очистка истории транзакций")
    def test_clear_transaction_history(
        self, driver_class: WebDriver, banking_test_data_class: dict[str, dict[str, str]]
    ) -> None:
        customer_data = banking_test_data_class["customer_data"]
        customer_full_name = f"{customer_data['first_name']} {customer_data['last_name']}"

        customer_page = BankingCustomerPage(driver_class)
        customer_page.click_home()
        home_page = BankingHomePage(driver_class)
        home_page.navigate_to_customer_login()
        customer_page.select_customer(customer_full_name).click_login()

        with allure.step("Нажать кнопку Transactions"):
            customer_page.click_transactions()

        with allure.step("Нажать кнопку Reset"):
            customer_page.click_reset()

        with allure.step("Проверить, что транзакции очистились"):
            assert customer_page.get_transactions_count() == ZERO, "Список транзакций не пуст после сброса"

        with allure.step("Нажать кнопку Back"):
            customer_page.click_back()

        with allure.step("Проверить состояние баланса Balance : 0"):
            assert customer_page.get_balance() == ZERO, f"Баланс не равен {ZERO} после очистки транзакций"

    @allure.title("5.4 Удаление покупателя")
    def test_delete_customer(self, driver_class: WebDriver, banking_test_data_class: dict[str, dict[str, str]]) -> None:
        customer_data = banking_test_data_class["customer_data"]

        customer_page = BankingCustomerPage(driver_class)
        customer_page.navigate_to_bank_manager_login_via_home()

        manager_page = BankingManagerPage(driver_class)

        with allure.step("Нажать кнопку Customers"):
            manager_page.click_customers()

        with allure.step("В поле поиска ввести First Name клиента"):
            manager_page.search_customer(customer_data["first_name"])

        with allure.step("Проверить, что он нашелся"):
            customer_rows = manager_page.get_customer_row_texts()
            assert any(customer_data["first_name"] in row for row in customer_rows), (
                f"Клиент {customer_data['first_name']} не найден перед удалением"
            )

        with allure.step("Нажать кнопку Delete"):
            manager_page.delete_customer()

        with allure.step("Очистить поле поиска"):
            manager_page.clear_search()

        with allure.step("Проверить, что в таблице он отсутствует"):
            customer_rows_after = manager_page.get_customer_row_texts()
            assert all(customer_data["first_name"] not in row for row in customer_rows_after), (
                f"Клиент {customer_data['first_name']} все еще присутствует в таблице после удаления"
            )
