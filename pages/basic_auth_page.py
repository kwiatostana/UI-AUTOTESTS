import base64

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class BasicAuthPage(BasePage):
    """Page Object для страницы Basic Auth"""

    DISPLAY_IMAGE_BUTTON = (By.ID, "displayImage")
    AUTHENTICATED_IMAGE = (By.CSS_SELECTOR, "img#downloadImg[src*='authenticatedimage']")

    @allure.step("Нажать на кнопку Display Image")
    def click_display_image(self) -> "BasicAuthPage":
        self.scroll_to_element(self.DISPLAY_IMAGE_BUTTON)
        self.click(self.DISPLAY_IMAGE_BUTTON)
        return self

    @allure.step("Пройти авторизацию Basic Auth (логин: {login})")
    def authenticate(self, login, password) -> "BasicAuthPage":
        auth_str = f"{login}:{password}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()

        self.driver.execute_cdp_cmd("Network.enable", {})
        self.driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
            "headers": {"Authorization": f"Basic {encoded_auth}"}
        })

        self.driver.refresh()

        self.click_display_image()
        return self

    @allure.step("Проверить, что секретное изображение отображается")
    def is_authenticated_image_displayed(self) -> bool:
        return self.is_displayed(self.AUTHENTICATED_IMAGE)
