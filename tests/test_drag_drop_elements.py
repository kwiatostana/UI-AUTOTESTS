import allure

from pages.drag_n_drop_page import DragNDropPage


@allure.epic("Пользовательский интерфейс")
@allure.feature("Drag and Drop")
@allure.story("Взаимодействие с элементами Drag and Drop")
@allure.severity(allure.severity_level.NORMAL)
@allure.id("TC_DRAG_DROP_001")
class TestDragDropElements:
    """Тест-кейс: Drag and Drop"""

    @allure.title("Проверка отображения всех основных элементов")
    def test_drag_and_drop_elements_are_displayed(self, opened_drag_n_drop_page: DragNDropPage) -> None:
        with allure.step("Проверить отображение всех элементов Drag and Drop"):
            opened_drag_n_drop_page.check_elements_are_displayed()

    @allure.title("Проверка функциональности Drag and Drop")
    def test_drag_and_drop_work(self, opened_drag_n_drop_page: DragNDropPage) -> None:
        with allure.step("Получить текст принимающего элемента до перетаскивания"):
            initial_text = opened_drag_n_drop_page.get_target_text()

        with allure.step("Перетащить элемент в целевую область"):
            opened_drag_n_drop_page.drag_element_to_target()

        with allure.step("Проверить, что текст принимающего элемента изменился"):
            current_text = opened_drag_n_drop_page.get_target_text()
            assert current_text != initial_text, (
                f"Текст не изменился. Ожидалось отличие от '{initial_text}', получено '{current_text}'"
            )
