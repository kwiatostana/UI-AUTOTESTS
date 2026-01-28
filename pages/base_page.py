from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.constants import DEFAULT_TIMEOUT, SCROLL_PIXELS_AMOUNT

Locator = tuple[str, str]


class BasePage:
    """Базовый класс для всех page objects"""

    POPUP_CLOSE_BUTTON: Locator = (By.CSS_SELECTOR, ".dialog-close-button.dialog-lightbox-close-button")

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> "BasePage":
        self.driver.get(url)
        return self

    def find_element(self, locator: Locator) -> WebElement:
        """Найти элемент с ожиданием присутствия в DOM"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator: Locator) -> list[WebElement]:
        """
        Найти все элементы с ожиданием.
        """
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []

    def click(self, locator: Locator) -> "BasePage":
        """Кликнуть по элементу с ожиданием кликабельности"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return self

    def js_click(self, locator: Locator) -> "BasePage":
        """
        Клик через JS.
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)
        return self

    def send_keys(self, locator: Locator, text: str) -> "BasePage":
        """
        Ввести текст.
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
        return self

    def get_text(self, locator: Locator) -> str:
        """Получить текст элемента"""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def get_attribute(self, locator: Locator, attribute: str) -> str:
        """Получить значение атрибута (например, value, href, class)"""
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    def is_displayed(self, locator: Locator) -> bool:
        """Проверить видимость элемента"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except TimeoutException:
            return False

    def is_present(self, locator: Locator) -> bool:
        """Проверить наличие элемента в DOM"""
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_enabled(self, locator: Locator) -> bool:
        """Проверить, активен ли элемент"""
        element = self.wait.until(EC.presence_of_element_located(locator))
        return element.is_enabled()

    def scroll_to_element(self, locator: Locator) -> "BasePage":
        """Прокрутить к элементу и дождаться его видимости"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.wait.until(EC.visibility_of_element_located(locator))
        return self

    def scroll_down(self, pixels: int = SCROLL_PIXELS_AMOUNT) -> "BasePage":
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")
        return self

    def wait_for_text(self, locator: Locator, text: str) -> bool:
        """Ожидать появления текста внутри элемента"""
        try:
            return self.wait.until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            return False

    def wait_for_alert(self) -> Alert | None:
        """Ожидать появления alert и вернуть его объект"""
        try:
            return self.wait.until(EC.alert_is_present())
        except TimeoutException:
            return None

    def accept_alert(self) -> "BasePage":
        """Принять alert"""
        if self.wait_for_alert():
            alert = self.driver.switch_to.alert
            alert.accept()
        return self

    def get_current_url(self) -> str:
        "Получить текущий url"
        return self.driver.current_url

    def close_popup(self, wait_timeout: int = 8) -> "BasePage":
        """Закрыть попап"""
        popup_wait = WebDriverWait(self.driver, wait_timeout)

        try:
            element = popup_wait.until(EC.element_to_be_clickable(self.POPUP_CLOSE_BUTTON))
            try:
                element.click()
            except Exception:
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                except Exception:
                    from selenium.webdriver.common.action_chains import \
                        ActionChains

                    ActionChains(self.driver).move_to_element(element).click().perform()
        except TimeoutException:
            pass

        return self
