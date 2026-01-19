"""Page Object для страницы Lifetime Membership"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LifetimeMembershipPage(BasePage):
    """Класс для работы со страницей Lifetime Membership"""

    LIFETIME_MEMBERSHIP_TEXT_LOCATOR = (By.CSS_SELECTOR, "h1.elementor-heading-title.elementor-size-default")
