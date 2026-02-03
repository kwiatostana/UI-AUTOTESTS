import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

"""Page Object для страницы Tabs"""


class TabsPage(BasePage):
    """Класс для работы со страницей Tabs"""

    LINK_TO_NEXT_PAGE = (By.CSS_SELECTOR, ".farme_window a")
    LINK_TO_NEXT_PAGE_2 = (By.CSS_SELECTOR, ".farme_window a")
    DEMO_FRAME = (By.CSS_SELECTOR, "iframe.demo-frame")

    @allure.step("Переключиться на фрейм с демо")
    def switch_to_demo_frame(self) -> "TabsPage":
        """Переключиться на фрейм с демо"""
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.DEMO_FRAME))
        return self

    @allure.step("Нажать на ссылку для перехода на следующую страницу")
    def click_link_to_next_page(self) -> "TabsPage":
        """Нажать на ссылку для перехода на следующую страницу"""
        self.click(self.LINK_TO_NEXT_PAGE)
        return self

    @allure.step("Переключиться на новую вкладку")
    def switch_to_new_tab(self) -> "TabsPage":
        """Переключиться на новую вкладку"""
        self.switch_to_new_window()
        return self

    @allure.step("Нажать на ссылку на новой странице")
    def click_link_to_next_page_2(self) -> "TabsPage":
        """Нажать на ссылку на новой странице"""
        self.click(self.LINK_TO_NEXT_PAGE_2)
        return self
