import allure

"""Page Object для главной страницы"""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class HomePage(BasePage):
    """Класс для работы с главной страницей"""

    HEADER_CONTACT = (By.CSS_SELECTOR, ".elementor-icon-list-items.elementor-inline-items")
    NAVIGATION_MENU = (By.ID, "site-navigation")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "a.elementor-button[href*='lifetime-membership-club']")
    COURSES_LIST = (By.CSS_SELECTOR, "div[data-id='259f3103']")
    FOOTER = (By.CSS_SELECTOR, "div[data-id='573bc308']")

    MAIN_ELEMENTS = {
        "HEADER_CONTACT": HEADER_CONTACT,
        "NAVIGATION_MENU": NAVIGATION_MENU,
        "REGISTER_BUTTON": REGISTER_BUTTON,
        "COURSES_LIST": COURSES_LIST,
        "FOOTER": FOOTER,
    }

    PHONE_NUMBERS = (By.XPATH, "//a[contains(@href, 'tel:') or contains(@href, 'wa.me')]")
    SKYPE_LINK = (By.XPATH, "//a[starts-with(@href, 'skype:')]")
    EMAIL = (By.XPATH, "//a[starts-with(@href, 'mailto:')]")
    SOCIAL_LINKS = (By.XPATH, "//i[contains(@class, 'fab')]/ancestor::a")

    COURSES_SLIDER = (By.CSS_SELECTOR, ".elementor-button.elementor-size-xs")
    SLIDER_NEXT_BUTTON = (By.CSS_SELECTOR, ".swiper-button-next-c50f9f0")
    SLIDER_PREV_BUTTON = (By.CSS_SELECTOR, ".swiper-button-prev-c50f9f0")

    FOOTER_ADDRESS = (
        By.XPATH,
        "//div[@data-id='695441a0']//span[@class='elementor-icon-list-text'][contains(normalize-space(.), 'CDR Complex')]",
    )
    FOOTER_PHONES = (By.CSS_SELECTOR, "div[data-id='695441a0'] a[href^='tel:']")
    FOOTER_EMAILS = (By.CSS_SELECTOR, "div[data-id='695441a0'] a[href^='mailto:']")

    ALL_COURSES_MENU = (By.ID, "menu-item-27580")
    LIFETIME_MEMBERSHIP_MENU = (By.ID, "menu-item-27581")

    @allure.step("Прокрутить к кнопке регистрации")
    def scroll_to_register_button(self) -> "HomePage":
        """Прокрутить к кнопке регистрации"""
        try:
            extended_wait = WebDriverWait(self.driver, 20)
            element = extended_wait.until(EC.visibility_of_element_located(self.REGISTER_BUTTON))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        except (TimeoutException, Exception):
            pass
        return self

    @allure.step("Переход на страницу Lifetime membership")
    def navigate_to_lifetime_membership(self) -> "HomePage":
        """Переход на страницу Lifetime membership"""
        self.click(self.ALL_COURSES_MENU).click(self.LIFETIME_MEMBERSHIP_MENU)
        return self

    @allure.step("Кликнуть по кнопке 'Вперед' слайдера")
    def click_slider_next(self) -> "HomePage":
        """Кликнуть по кнопке 'Вперед' слайдера"""
        self.scroll_to_element(self.SLIDER_NEXT_BUTTON)
        self.click(self.SLIDER_NEXT_BUTTON)
        return self

    @allure.step("Кликнуть по кнопке 'Назад' слайдера")
    def click_slider_prev(self) -> "HomePage":
        """Кликнуть по кнопке 'Назад' слайдера"""
        self.scroll_to_element(self.SLIDER_PREV_BUTTON)
        self.click(self.SLIDER_PREV_BUTTON)
        return self

    @allure.step("Получить href активного слайда")
    def get_active_slide_href(self) -> str:
        """Получить href активного (видимого) слайда"""
        slides = self.find_elements(self.COURSES_SLIDER)
        for slide in slides:
            if slide.is_displayed():
                href = slide.get_attribute("href")
                if href:
                    return href
        return ""

    @allure.step("Подождать изменения href активного слайда")
    def wait_for_slider_change(self, initial_href: str) -> str:
        """
        Ожидает, пока href активного слайда не изменится по сравнению с initial_href.
        Возвращает новый href.
        """
        try:
            self.wait.until(
                lambda _: any(
                    slide.is_displayed() and slide.get_attribute("href") != initial_href
                    for slide in self.find_elements(self.COURSES_SLIDER)
                )
            )
        except TimeoutException:
            pass
        return self.get_active_slide_href()

    @allure.step("Подождать совпадения href активного слайда")
    def wait_for_slider_match(self, expected_href: str) -> str:
        """
        Ожидает, пока href активного слайда не станет равен expected_href.
        Возвращает текущий href.
        """
        try:
            self.wait.until(
                lambda _: any(
                    slide.is_displayed() and slide.get_attribute("href") == expected_href
                    for slide in self.find_elements(self.COURSES_SLIDER)
                )
            )
        except TimeoutException:
            pass
        return self.get_active_slide_href()

    @allure.step("Убедиться, что все нужные элементы отображаются")
    def check_elements_are_displayed(self) -> "HomePage":
        for name, locator in self.MAIN_ELEMENTS.items():
            with allure.step(f"Проверить отображение элемента {name}"):
                if name == "REGISTER_BUTTON":
                    self.scroll_to_register_button()
                assert self.is_displayed(locator), f"Элемент {name} не отображается"
