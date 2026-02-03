import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

"""Page Object для страницы Drag and Drop"""


class DragNDropPage(BasePage):
    """Класс для работы со страницей Drag and Drop"""

    DRAGGABLE = (By.ID, "draggable")
    DROPPABLE = (By.ID, "droppable")
    DEMO_FRAME = (By.CSS_SELECTOR, "iframe.demo-frame")

    MAIN_ELEMENTS = {
        "DRAGGABLE": DRAGGABLE,
        "DROPPABLE": DROPPABLE,
    }

    @allure.step("Переключиться на фрейм с демо")
    def switch_to_demo_frame(self) -> "DragNDropPage":
        """Переключиться на фрейм с демо"""
        try:
            self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.DEMO_FRAME))
        except Exception:
            try:
                self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
            except Exception:
                pass
        return self

    @allure.step("Перетащить элемент в принимающий блок")
    def drag_element_to_target(self) -> "DragNDropPage":
        """Перетащить элемент в принимающий блок"""
        source = self.find_element(self.DRAGGABLE)
        target = self.find_element(self.DROPPABLE)

        actions = ActionChains(self.driver)
        actions.drag_and_drop(source, target).perform()
        return self

    @allure.step("Получить текст принимающего элемента")
    def get_target_text(self) -> str:
        """Получить текст принимающего элемента"""
        return self.get_text(self.DROPPABLE)

    @allure.step("Убедиться, что все нужные элементы отображаются")
    def check_elements_are_displayed(self) -> "DragNDropPage":
        """Проверить отображение основных элементов"""
        for name, locator in self.MAIN_ELEMENTS.items():
            with allure.step(f"Проверить отображение элемента {name}"):
                assert self.is_displayed(locator), f"Элемент {name} не отображается"
        return self
