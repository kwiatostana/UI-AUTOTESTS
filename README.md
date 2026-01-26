## Web Testing Automation
Набор автотестов для проверки UI. Проект выполнен для SimbirSoft.

### Технологический стек
- Python 3.10+
- Pytest — запуск и управление тестами
- Selenium WebDriver — автоматизация браузера
- webdriver-manager — автоматическое управление драйверами
- python-dotenv — конфигурация через `.env`
- allure-pytest — генерация Allure-отчётов

### Структура проекта
```text
U1_tests/
├── pages/                  # Page Object классы
│   ├── base_page.py        # Базовый класс с общими методами (явные ожидания, базовые действия)
│   ├── home_page.py        # Главная страница Way2Automation
│   ├── login_page.py       # Страница авторизации
│   ├── banking_home_page.py # Главная страница банковского приложения
│   ├── banking_customer_page.py # Страница клиента банка
│   ├── banking_manager_page.py # Страница менеджера банка
│   ├── lifetime_membership_page.py # Страница клуба Lifetime Membership
│   └── sample_form_page.py # Sample Form
├── tests/                  # Тестовые сценарии
│   ├── conftest.py         # Фикстуры
│   ├── test_home_page_ui.py # Проверки UI главной страницы
│   ├── test_sticky_menu.py # Проверка фиксации меню при скроллинге
│   ├── test_navigation_transition.py # Тесты переходов по разделам
│   ├── test_login_validation.py # Валидация формы логина
│   └── test_banking_e2e.py # е2е сценарий работы с банком
├── src/                    # Глобальные константы и настройки
│   └── constants.py        # Константы
├── utils/                  # Вспомогательные инструменты
│   └── data_generator.py   # Генераторы уникальных тестовых данных
├── .env.example            # Пример файла с переменными окружения
├── pytest.ini              # Конфигурация запуска pytest
├── README.md               # Документация проекта
└── requirements.txt        # Список зависимостей
```

### Быстрый старт

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/kwiatostana/UI-AUTOTESTS
   cd UI-AUTOTESTS
   ```

2. **Настройте виртуальное окружение:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

Создайте файл `.env` в корне проекта с валидными данными

```

### Запуск тестов

- **Все тесты:** `pytest`
- **Конкретный файл:** `pytest tests/test_banking_e2e.py`
- **С генерацией Allure-отчета:**
  ```bash
  pytest --alluredir=allure-results
  allure serve allure-results
  ```

### Архитектурные особенности
- **Page Object Model (POM)**: Логика взаимодействия вынесена в отдельные классы.
- **Fluent Interface**: Методы страниц возвращают `self` для поддержки цепочек вызовов.
- **Явные ожидания (Explicit Waits)**: Используется `WebDriverWait` для всех взаимодействий.
- **Динамические данные**: Использование уникальных данных (Faker) для каждого запуска.
- **Автоматическая очистка**: Фикстуры обеспечивают удаление созданных данных после тестов.
