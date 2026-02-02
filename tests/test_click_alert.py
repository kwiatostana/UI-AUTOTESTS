import allure

from pages.alerts_page import AlertsPage
from utils.data_generator import generate_random_name


@allure.epic("Пользовательский интерфейс")
@allure.feature("Alert")
@allure.story("Взаимодействие с Input Alert")
@allure.severity(allure.severity_level.NORMAL)
@allure.id("TC_ALERTS_001")
class TestAlerts:
    """Тест-кейс: Взаимодействие с Input Alert"""

    @allure.title("Ввод имени в Input Alert и проверка отображения")
    def test_input_alert_name(self, opened_alerts_page: AlertsPage) -> None:
        name = generate_random_name()

        with allure.step("Перейти на вкладку Input Alert и проверить, что кнопка видна"):
            opened_alerts_page.click_input_alert_link()
            opened_alerts_page.switch_to_demo_frame()
            assert opened_alerts_page.is_displayed(opened_alerts_page.INPUT_BOX_BUTTON), (
                "Кнопка не отображается"
            )

        with allure.step(f"Ввести имя '{name}' в Alert"):
            opened_alerts_page.click_input_box_button()
            opened_alerts_page.send_keys_to_alert(name)

        with allure.step(f"Убедиться, что результат содержит имя '{name}'"):
            result_text = opened_alerts_page.get_result_text()
            assert name in result_text, f"Ожидалось, что имя '{name}' будет в тексте '{result_text}'"
            assert result_text == f"Hello {name}! How are you today?", "Текст приветствия не совпадает с ожидаемым"
