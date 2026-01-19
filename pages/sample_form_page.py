from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class SampleFormPage(BasePage):
    """Класс для работы со страницей Sample Form"""

    FIRST_NAME_FIELD = (By.ID, "firstName")
    LAST_NAME_FIELD = (By.ID, "lastName")
    EMAIL_FIELD = (By.ID, "email")
    PASSWORD_FIELD = (By.ID, "password")

    HOBBIES_LABELS = (By.CSS_SELECTOR, "div.checkbox-group label")
    HOBBY_SPORTS = (By.CSS_SELECTOR, "input[value='Sports']")

    GENDER_DROPBOX = (By.ID, "gender")

    ABOUT_YOURSELF_FIELD = (By.ID, "about")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_MESSAGE = (By.ID, "successMessage")

    def fill_registration_form(self, first_name: str, last_name: str, email: str, password: str) -> "SampleFormPage":
        """Заполнить основные поля формы"""
        return (
            self.send_keys(self.FIRST_NAME_FIELD, first_name)
            .send_keys(self.LAST_NAME_FIELD, last_name)
            .send_keys(self.EMAIL_FIELD, email)
            .send_keys(self.PASSWORD_FIELD, password)
        )

    def select_hobby(self) -> "SampleFormPage":
        """Выбрать хобби"""
        checkbox = self.find_element(self.HOBBY_SPORTS)

        if not checkbox.is_selected():
            checkbox.click()

        return self

    def select_gender(self, value: str) -> "SampleFormPage":
        """Выбрать пол в выпадающем списке"""
        dropdown = self.find_element(self.GENDER_DROPBOX)
        select = Select(dropdown)
        select.select_by_value(value)
        return self

    def get_hobby_words(self) -> list[str]:
        """Получить список текстов всех доступных хобби"""
        hobbies_elements = self.find_elements(self.HOBBIES_LABELS)
        hobbies_texts = [elem.text.strip() for elem in hobbies_elements if elem.text.strip()]
        return hobbies_texts

    def submit_registration(self) -> "SampleFormPage":
        """Нажать кнопку Register"""
        self.scroll_to_element(self.REGISTER_BUTTON)
        self.click(self.REGISTER_BUTTON)
        return self
