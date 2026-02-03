## Web Testing Automation
Набор автотестов для проверки UI. Проект выполнен для SimbirSoft.

### Технологический стек
- Python 3.10+
- Pytest — запуск и управление тестами
- Selenium WebDriver 4.15+ — автоматизация браузера (встроенный Selenium Manager для драйверов)
- Selenium Grid — распределённый запуск тестов
- python-dotenv — конфигурация через `.env`
- allure-pytest — генерация Allure-отчётов
- pytest-xdist — параллельный запуск тестов

### Поддерживаемые браузеры
- Google Chrome
- Mozilla Firefox
- Microsoft Edge

Драйверы скачиваются автоматически через Selenium Manager (Selenium 4.6+).

### Структура проекта
```text
UI_AUTOTESTS/
├── pages/                  # Page Object классы
│   ├── base_page.py        # Базовый класс с общими методами
│   ├── home_page.py        # Главная страница Way2Automation
│   ├── login_page.py       # Страница авторизации
│   ├── banking_home_page.py
│   ├── banking_customer_page.py
│   ├── banking_manager_page.py
│   └── ...
├── testcases/              # Тест-кейсы
├── tests/                  # Тестовые сценарии
├── src/                    # Глобальные константы и настройки
│   └── constants.py
├── utils/                  # Вспомогательные инструменты
│   └── data_generator.py
├── grid/                   # Selenium Grid
│   ├── selenium-server.jar # Selenium Server
│   ├── start_hub.bat       # Запуск Hub (Windows)
│   └── start_node.bat      # Запуск Node (Windows)
├── .env.example            # Пример настроек окружения
├── conftest.py             # Фикстуры pytest
├── driver_factory.py       # Фабрика для создания WebDriver
├── pytest.ini              # Конфигурация pytest
├── README.md               # Описание проекта
├── requirements.txt        # Зависимости
├── run_failed.bat          # Запуск упавших тестов
└── run_failed.ps1          # Запуск упавших тестов
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

4. **Создайте файл `.env`** в корне проекта с валидными данными.

### Запуск тестов

#### Локальный запуск

```bash
# Chrome
pytest --executor=local

# Firefox
pytest --browser=firefox --executor=local

# Edge
pytest --browser=edge --executor=local

# Конкретный файл
pytest tests/test_banking_e2e.py --browser=chrome --executor=local
```

#### Запуск через Selenium Grid

1. **Запустите Selenium Grid**:
   ```bash
   # Терминал 1 — запуск Hub
   grid\start_hub.bat

   # Терминал 2 — запуск Node
   grid\start_node.bat
   ```

   Grid UI доступен по адресу: http://localhost:4444

2. **Запустите тесты:**
   ```bash
   # Chrome через Grid
   pytest --browser=chrome --executor=grid

   # Firefox через Grid
   pytest --browser=firefox --executor=grid

   # Edge через Grid
   pytest --browser=edge --executor=grid

   # Указать другой URL Grid
   pytest --executor=grid --grid-url=http://192.168.1.100:4444
   ```

#### Параллельный запуск

```bash
# 2 параллельных воркера
pytest -n 2

# Автоматическое определение числа воркеров
pytest -n auto
```

#### Allure-отчёты

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

### Архитектурные особенности
- **Page Object Model (POM)**: Логика взаимодействия вынесена в отдельные классы
- **DriverFactory**: Паттерн Factory для создания драйверов разных браузеров
- **Selenium Grid**: Поддержка распределённого запуска тестов
- **Явные ожидания**: `WebDriverWait` для всех взаимодействий
- **Параллельный запуск**: pytest-xdist для ускорения тестов
- **Автоматический перезапуск**: pytest-rerunfailures для упавших тестов
