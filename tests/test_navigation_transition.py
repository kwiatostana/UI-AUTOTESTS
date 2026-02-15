import allure
import pytest

from pages.home_page import HomePage
from pages.lifetime_membership_page import LifetimeMembershipPage
from src.constants import (LIFETIME_MEMBERSHIP_CLUB_TEXT,
                           LIFETIME_MEMBERSHIP_URL)

@pytest.mark.ci
@allure.epic("Навигация")
@allure.feature("Переходы по страницам")
@allure.story("Переход на страницу Lifetime membership")
@allure.severity(allure.severity_level.NORMAL)
@allure.id("TC_NAV_TRANSITION_003")
class TestNavigationTransition:
    """Тест-кейс 3: Проверка перехода по меню навигации"""

    @allure.title("Проверка перехода на страницу Lifetime membership")
    def test_navigation_to_lifetime_membership_page(self, opened_home_page: HomePage) -> None:
        opened_home_page.navigate_to_lifetime_membership()

        with allure.step("Проверить открытие страницы (URL и заголовок)"):
            current_url = opened_home_page.get_current_url()
            assert current_url == LIFETIME_MEMBERSHIP_URL, (
                f"Ожидался URL {LIFETIME_MEMBERSHIP_URL}, получен {current_url}"
            )

            lifetime_membership_page = LifetimeMembershipPage(opened_home_page.driver)
            h1_text = lifetime_membership_page.get_text(lifetime_membership_page.LIFETIME_MEMBERSHIP_TEXT_LOCATOR)
            assert LIFETIME_MEMBERSHIP_CLUB_TEXT in h1_text, (
                f"Текст '{LIFETIME_MEMBERSHIP_CLUB_TEXT}' не найден. Получен текст: '{h1_text}'"
            )
