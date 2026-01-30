import allure

from pages.sample_form_page import SampleFormPage
from src.constants import JS_USERNAME


@allure.epic("Технические функции")
@allure.feature("JS-утилиты")
@allure.story("Работа JS-утилит через execute_script")
@allure.severity(allure.severity_level.MINOR)
@allure.id("TC_JS_UTILS_001")
class TestJSUtils:
    """Тест-кейс 6: Проверка работы JS-утилит через execute_script"""

    @allure.title("Проверка работы JS-утилит: снятие фокуса и проверка скролла")
    def test_js_utilities_blur_and_scroll(self, opened_sample_form_page: SampleFormPage) -> None:

        with allure.step(f'Ввести "{JS_USERNAME}" в поле First Name'):
            opened_sample_form_page.send_keys(
                opened_sample_form_page.FIRST_NAME_FIELD,
                JS_USERNAME
            )

        with allure.step("Проверить, что поле First Name находится в фокусе"):
            is_focused_before = opened_sample_form_page.is_element_focused(
                opened_sample_form_page.FIRST_NAME_FIELD
            )
            assert is_focused_before, "Поле First Name должно быть в фокусе после ввода текста"

        with allure.step("Снять фокус с поля First Name через JS"):
            opened_sample_form_page.blur_element(opened_sample_form_page.FIRST_NAME_FIELD)

        with allure.step("Проверить, что фокус убран с поля First Name"):
            is_focused_after = opened_sample_form_page.is_element_focused(
                opened_sample_form_page.FIRST_NAME_FIELD
            )
            assert not is_focused_after, "Поле First Name не должно быть в фокусе после вызова blur()"

        with allure.step("Проверить наличие вертикального скролла на странице"):
            has_scroll = opened_sample_form_page.has_vertical_scroll()
            assert has_scroll, "На странице должен присутствовать вертикальный скролл"
