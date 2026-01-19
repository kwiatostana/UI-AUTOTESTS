import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from pages.home_page import HomePage
from src.constants import DEFAULT_TIMEOUT, ZERO


@allure.feature("Тесты главной страницы")
class TestHomePageUI:
    """Тест-кейс 1: Главная страница"""

    @allure.title("Проверка отображения всех основных элементов")
    def test_main_page_elements_are_displayed(self, opened_home_page: HomePage) -> None:
        elements = {
            "HEADER_CONTACT": opened_home_page.HEADER_CONTACT,
            "NAVIGATION_MENU": opened_home_page.NAVIGATION_MENU,
            "REGISTER_BUTTON": opened_home_page.REGISTER_BUTTON,
            "COURSES_LIST": opened_home_page.COURSES_LIST,
            "FOOTER": opened_home_page.FOOTER,
        }

        for name, locator in elements.items():
            with allure.step(f"Проверить отображение элемента {name}"):
                if name == "REGISTER_BUTTON":
                    opened_home_page.scroll_to_register_button()
                assert opened_home_page.is_displayed(locator), f"Элемент {name} не отображается"

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
        with allure.step("Прокрутить к слайдеру курсов"):
            opened_home_page.scroll_to_element(opened_home_page.COURSES_SLIDER)

        with allure.step("Получить href начального слайда"):
            slides = opened_home_page.find_elements(opened_home_page.COURSES_SLIDER)
            initial_href = ""
            for slide in slides:
                if slide.is_displayed():
                    href = slide.get_attribute("href")
                    if href:
                        initial_href = href
                        break
            assert initial_href, "Не удалось получить ссылку (href) активного слайда"

        with allure.step("Проверить работу кнопки 'Вперед' слайдера"):
            opened_home_page.click_slider_next()
            wait = WebDriverWait(opened_home_page.driver, DEFAULT_TIMEOUT)
            try:
                wait.until(
                    lambda _: any(
                        slide.is_displayed() and slide.get_attribute("href") != initial_href
                        for slide in opened_home_page.find_elements(opened_home_page.COURSES_SLIDER)
                    )
                )
            except TimeoutException:
                pass

            slides = opened_home_page.find_elements(opened_home_page.COURSES_SLIDER)
            after_next_href = ""
            for slide in slides:
                if slide.is_displayed():
                    href = slide.get_attribute("href")
                    if href:
                        after_next_href = href
                        break
            assert after_next_href != initial_href, (
                f"Href не изменился после нажатия 'Вперед'. Ожидалось отличие от {initial_href}, получено {after_next_href}"
            )

        with allure.step("Проверить работу кнопки 'Назад' слайдера"):
            opened_home_page.click_slider_prev()
            wait = WebDriverWait(opened_home_page.driver, DEFAULT_TIMEOUT)
            try:
                wait.until(
                    lambda _: any(
                        slide.is_displayed() and slide.get_attribute("href") != after_next_href
                        for slide in opened_home_page.find_elements(opened_home_page.COURSES_SLIDER)
                    )
                )
            except TimeoutException:
                pass

            slides = opened_home_page.find_elements(opened_home_page.COURSES_SLIDER)
            after_prev_href = ""
            for slide in slides:
                if slide.is_displayed():
                    href = slide.get_attribute("href")
                    if href:
                        after_prev_href = href
                        break
            assert after_prev_href == initial_href, (
                f"Href не вернулся к исходному значению после нажатия 'Назад'. Ожидалось {initial_href}, получено {after_prev_href}"
            )

    @allure.title("Проверка наличия необходимой информации")
    def test_footer_contains_required_information(self, opened_home_page: HomePage) -> None:
        with allure.step("Прокрутить к футеру"):
            opened_home_page.scroll_to_element(opened_home_page.FOOTER)

        with allure.step("Проверить отображение футера"):
            assert opened_home_page.is_displayed(opened_home_page.FOOTER), "Футер не отображается"

        with allure.step("Проверить отображение адреса в футере"):
            assert opened_home_page.is_displayed(opened_home_page.FOOTER_ADDRESS), "Адрес не отображается в футере"

        with allure.step("Проверить наличие телефонов в футере"):
            phones = opened_home_page.find_elements(opened_home_page.FOOTER_PHONES)
            assert len(phones) > ZERO, f"В футере должно быть больше {ZERO} телефонов, но найдено {len(phones)}"

        with allure.step("Проверить наличие email адресов в футере"):
            emails = opened_home_page.find_elements(opened_home_page.FOOTER_EMAILS)
            assert len(emails) > ZERO, f"В футере должно быть больше {ZERO} email адресов, но найдено {len(emails)}"
