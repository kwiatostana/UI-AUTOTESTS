import allure

from pages.tabs_page import TabsPage
from src.constants import (EXPECTED_WINDOWS_COUNT_THREE,
                           EXPECTED_WINDOWS_COUNT_TWO, TABS_URL)


@allure.epic("Пользовательский интерфейс")
@allure.feature("Страница Tabs")
@allure.story("Взаимодействие с элементами Tabs")
@allure.severity(allure.severity_level.NORMAL)
@allure.id("TC_TABS_001")
class TestChangeTabs:
    """Тест-кейс: Tabs"""

    @allure.title("Проверка переключения между вкладками и нажатия ссылок")
    def test_change_tabs_and_click_links(self, opened_tabs_page: TabsPage) -> None:
        driver = opened_tabs_page.driver

        with allure.step("Нажать на первую ссылку"):
            opened_tabs_page.click_link_to_next_page()

        with allure.step("Проверить, что открылось второе окно"):
            assert len(driver.window_handles) == EXPECTED_WINDOWS_COUNT_TWO, f"Ожидалось {EXPECTED_WINDOWS_COUNT_TWO} окна, но открыто {len(driver.window_handles)}"

        with allure.step("Переключиться на вторую вкладку"):
            opened_tabs_page.switch_to_new_tab()
            current_url = opened_tabs_page.get_current_url()
            assert current_url != TABS_URL, f"URL новой вкладки не должен совпадать с {TABS_URL}"

        with allure.step("Нажать на вторую ссылку на новой странице"):
            opened_tabs_page.click_link_to_next_page_2()

        with allure.step("Проверить, что открылось третье окно"):
            assert len(driver.window_handles) == EXPECTED_WINDOWS_COUNT_THREE, f"Ожидалось {EXPECTED_WINDOWS_COUNT_THREE} окна, но открыто {len(driver.window_handles)}"
