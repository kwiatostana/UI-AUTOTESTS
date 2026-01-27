import allure

from pages.home_page import HomePage
from src.constants import ZERO


@allure.epic("Пользовательский интерфейс")
@allure.feature("Главная страница")
@allure.story("Отображение элементов и навигация на главной странице")
@allure.severity(allure.severity_level.NORMAL)
@allure.id("TC_MAIN_PAGE_001")
class TestHomePageUI:
    """Тест-кейс 1: Главная страница"""

    @allure.title("Проверка отображения всех основных элементов")
    def test_main_page_elements_are_displayed(self, opened_home_page: HomePage) -> None:
        opened_home_page.check_elements_are_displayed()

    @allure.title("Проверка наличия контактной информации")
    def test_header_contains_contact_information(self, opened_home_page: HomePage) -> None:
        with allure.step("Проверить наличие телефонных номеров в хедере"):
            assert opened_home_page.is_displayed(opened_home_page.PHONE_NUMBERS), (
                "Телефонные номера не отображаются в хедере"
            )

        with allure.step("Проверить наличие Skype ссылки в хедере"):
            assert opened_home_page.is_displayed(opened_home_page.SKYPE_LINK), "Skype ссылка не отображается в хедере"

        with allure.step("Проверить наличие email в хедере"):
            assert opened_home_page.is_displayed(opened_home_page.EMAIL), "Email адрес не отображается в хедере"

        with allure.step("Проверить наличие социальных ссылок в хедере"):
            assert opened_home_page.is_displayed(opened_home_page.SOCIAL_LINKS), (
                "Социальные ссылки не отображаются в хедере"
            )

    @allure.title("Проверка работы навигации")
    def test_courses_slider_navigation_works(self, opened_home_page: HomePage) -> None:
        opened_home_page.scroll_to_element(opened_home_page.COURSES_SLIDER)

        with allure.step("Получить href начального слайда"):
            initial_href = opened_home_page.get_active_slide_href()
            assert initial_href, "Не удалось получить ссылку (href) активного слайда"

        opened_home_page.click_slider_next()

        with allure.step("Проверить изменение href после нажатия 'Вперед'"):
            after_next_href = opened_home_page.wait_for_slider_change(initial_href)
            assert after_next_href != initial_href, (
                f"Href не изменился после нажатия 'Вперед'. Ожидалось отличие от {initial_href}, получено {after_next_href}"
            )

        opened_home_page.click_slider_prev()

        with allure.step("Проверить возврат к исходному href после нажатия 'Назад'"):
            after_prev_href = opened_home_page.wait_for_slider_match(initial_href)
            assert after_prev_href == initial_href, (
                f"Href не вернулся к исходному значению после нажатия 'Назад'. Ожидалось {initial_href}, получено {after_prev_href}"
            )

    @allure.title("Проверка наличия необходимой информации")
    def test_footer_contains_required_information(self, opened_home_page: HomePage) -> None:
        opened_home_page.scroll_to_element(opened_home_page.FOOTER)

        with allure.step("Проверить отображение футера и контактных данных в нем"):
            assert opened_home_page.is_displayed(opened_home_page.FOOTER), "Футер не отображается"
            assert opened_home_page.is_displayed(opened_home_page.FOOTER_ADDRESS), "Адрес не отображается в футере"

            phones = opened_home_page.find_elements(opened_home_page.FOOTER_PHONES)
            assert len(phones) > ZERO, f"В футере должно быть больше {ZERO} телефонов, но найдено {len(phones)}"

            emails = opened_home_page.find_elements(opened_home_page.FOOTER_EMAILS)
            assert len(emails) > ZERO, f"В футере должно быть больше {ZERO} email адресов, но найдено {len(emails)}"
