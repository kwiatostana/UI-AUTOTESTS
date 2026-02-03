import os

from dotenv import load_dotenv

load_dotenv()

HOME_URL = os.getenv("HOME_URL")
LOGIN_URL = os.getenv("LOGIN_URL")
BANKING_URL = os.getenv("BANKING_URL")
SAMPLE_FORM_URL = os.getenv("SAMPLE_FORM_URL")
LIFETIME_MEMBERSHIP_URL = os.getenv("LIFETIME_MEMBERSHIP_URL")
BANKING_CUSTOMER_URL = os.getenv("BANKING_CUSTOMER_URL")
BANKING_MANAGER_URL = os.getenv("BANKING_MANAGER_URL")
COOKIES_URL = os.getenv("COOKIES_URL")
DRAG_N_DROP_URL = os.getenv("DRAG_N_DROP_URL")
TABS_URL = os.getenv("TABS_URL")
ALERTS_URL = os.getenv("ALERTS_URL")
BASIC_AUTH_URL = os.getenv("BASIC_AUTH_URL")

VALID_USERNAME = os.getenv("VALID_USERNAME")
VALID_PASSWORD = os.getenv("VALID_PASSWORD")

INVALID_USERNAME = "invalid_user"
INVALID_PASSWORD = "invalid_pass"

SUCCESS_LOGIN_MESSAGE = "You're logged in!!"
ERROR_LOGIN_MESSAGE = "Username or password is incorrect"
REGISTRATION_SUCCESS_MESSAGE = "User registered successfully!"
DEPOSIT_SUCCESS_MESSAGE = "Deposit Successful"
WITHDRAWAL_SUCCESS_MESSAGE = "Transaction successful"
WITHDRAWAL_FAILED_MESSAGE = "Transaction Failed. You can not withdraw amount more than the balance."

DEPOSIT_AMOUNT = int(os.getenv("DEPOSIT_AMOUNT"))
WITHDRAWAL_AMOUNT_LARGE = int(os.getenv("WITHDRAWAL_AMOUNT_LARGE"))

ZERO = 0
MIN_WITHDRAWAL_AMOUNT = 1
SCROLL_PIXELS_AMOUNT = 1000

DEFAULT_TIMEOUT = 5
POPUP_TIMEOUT = 10

LIFETIME_MEMBERSHIP_CLUB_TEXT = "LIFETIME MEMBERSHIP CLUB"

HOBBY_SPORTS = "Sports"
GENDER_FEMALE = "female"

POST_CODE_LENGTH = 5

EXPECTED_WINDOWS_COUNT_TWO = 2
EXPECTED_WINDOWS_COUNT_THREE = 3

BASIC_AUTH_LOGIN = os.getenv("BASIC_AUTH_LOGIN")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD") #пароль подходит любой абсолютно, но сработает 1 раз на открытие страницы, использую пароль из условий задания, для нескольких попыток подряд нужно генерить рандомный пароль

COOKIES_LOGIN = os.getenv("COOKIES_LOGIN")
COOKIES_PASSWORD = os.getenv("COOKIES_PASSWORD")
COOKIE_FILE_PATH = "state/cookies.json"

JS_USERNAME = "AutoTester"
