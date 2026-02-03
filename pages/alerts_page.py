import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

"""Page Object для страницы Alerts"""


class AlertsPage(BasePage):
    """Класс для работы со страницей Alerts"""

    INPUT_ALERT_LINK = (By.CSS_SELECTOR, "a[href='#example-1-tab-2']")
    INPUT_BOX_BUTTON = (By.CSS_SELECTOR, "button[onclick='myFunction()']")
    DEMO_FRAME = (By.CSS_SELECTOR, "#example-1-tab-2 iframe.demo-frame")
    TEXT_WITH_INPUT_NAME = (By.ID, "demo")

    @allure.step("Переключиться на фрейм с демо")
    def switch_to_demo_frame(self) -> "AlertsPage":
        """Переключиться на фрейм с демо"""
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.DEMO_FRAME))
        return self

    @allure.step("Нажать на ссылку Input Alert")
    def click_input_alert_link(self) -> "AlertsPage":
        self.click(self.INPUT_ALERT_LINK)
        return self

    @allure.step("Нажать на кнопку вызова Input Alert")
    def click_input_box_button(self) -> "AlertsPage":
        self.click(self.INPUT_BOX_BUTTON)
        return self

    @allure.step("Получить текст результата ввода в Alert")
    def get_result_text(self) -> str:
        return self.get_text(self.TEXT_WITH_INPUT_NAME)
