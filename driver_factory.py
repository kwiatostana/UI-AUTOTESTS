from typing import Literal

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class DriverFactory:
    """Фабрика для создания WebDriver различных браузеров"""

    SUPPORTED_BROWSERS = ["chrome", "firefox", "edge"]

    @staticmethod
    def create_driver(
        browser_name: Literal["chrome", "firefox", "edge"] = "chrome",
        use_grid: bool = False,
        grid_url: str = "http://localhost:4444",
        headless: bool = False
    ) -> WebDriver:

        browser_name = browser_name.lower()

        if browser_name not in DriverFactory.SUPPORTED_BROWSERS:
            raise ValueError(
                f"Браузер '{browser_name}' не поддерживается. "
                f"Доступные: {', '.join(DriverFactory.SUPPORTED_BROWSERS)}"
            )

        options = DriverFactory._get_browser_options(browser_name, headless=headless)

        if use_grid:
            driver = DriverFactory._create_remote_driver(grid_url, options)
        else:
            driver = DriverFactory._create_local_driver(browser_name, options)

        return driver

    @staticmethod
    def _get_browser_options(browser_name: str, headless: bool = False):
        """Создает options для указанного браузера"""

        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--window-size=1920,1080")

        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            options.set_preference("dom.webnotifications.enabled", False)
            options.set_preference("dom.push.enabled", False)

        elif browser_name == "edge":
            options = webdriver.EdgeOptions()
            options.add_argument("--start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

        return options

    @staticmethod
    def _create_remote_driver(grid_url: str, options) -> WebDriver:
        """Создает Remote WebDriver для Selenium Grid"""
        print(f"[GRID] Подключение к: {grid_url}")
        driver = webdriver.Remote(
            command_executor=grid_url,
            options=options
        )
        driver.maximize_window()
        return driver

    @staticmethod
    def _create_local_driver(browser_name: str, options) -> WebDriver:
        """
        Создает локальный WebDriver
        """
        print(f"[LOCAL] Запуск браузера: {browser_name}")

        if browser_name == "chrome":
            driver = webdriver.Chrome(options=options)

        elif browser_name == "firefox":
            driver = webdriver.Firefox(options=options)
            driver.maximize_window()

        elif browser_name == "edge":
            driver = webdriver.Edge(options=options)

        return driver
