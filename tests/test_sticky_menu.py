import allure

from pages.home_page import HomePage


@allure.epic("Пользовательский интерфейс")
@allure.feature("Навигационное меню")
@allure.story("Закрепленное меню при скроллинге")
@allure.severity(allure.severity_level.MINOR)
@allure.id("TC_NAV_SCROLL_002")
class TestStickyMenu:
    """Тест-кейс 2: Меню навигации при скроллинге"""

    @allure.title("Проверка отображения меню при скроллинге")
    def test_sticky_menu_remains_visible_on_scroll(self, opened_home_page: HomePage) -> None:
        with allure.step("Проверить отображение меню при скроллинге страницы"):
            opened_home_page.scroll_down()
            assert opened_home_page.is_displayed(opened_home_page.NAVIGATION_MENU), (
                "Меню навигации должно было оставаться видимым при скроллинге"
            )
