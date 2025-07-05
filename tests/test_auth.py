import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from utils.auth import login_user

@pytest.fixture(scope="module")
def driver():
    """Фикстура для инициализации и закрытия браузера"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)  # Не рекомендуется смешивать с явными ожиданиями
    yield driver
    driver.quit()

@pytest.fixture
def screenshots_dir():
    """Фикстура для создания папки со скриншотами"""
    os.makedirs("screenshots", exist_ok=True)
    return "screenshots"

def take_screenshot(driver, name="", screenshots_dir="screenshots"):
    """Утилита для создания скриншотов с timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{name}.png" if name else f"{timestamp}.png"
    path = os.path.join(screenshots_dir, filename)
    driver.save_screenshot(path)
    return path

def test_user_login(driver, screenshots_dir):
    """Тест авторизации пользователя"""
    try:
        # 1. Открытие сайта и обработка куки
        driver.get("https://frontend-develop.kube.artforintrovert.ru/")
        take_screenshot(driver, "01_initial_page", screenshots_dir)

        # Обработка куки-баннера
        try:
            cookie_banner = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.cookie-consent")))
            accept_btn = cookie_banner.find_element(By.CSS_SELECTOR, "button")
            accept_btn.click()
            take_screenshot(driver, "02_cookie_banner_accepted", screenshots_dir)
        except Exception as e:
            print(f"Cookie banner not found: {e}")
            take_screenshot(driver, "02_cookie_banner_not_found", screenshots_dir)

        # 2. Нажатие на кнопку "Войти" в хедере
        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(@class, 'afi-button') and contains(., 'Войти')]"
                ))
            )
            login_button.click()
            take_screenshot(driver, "03_login_button_clicked", screenshots_dir)
        except Exception as e:
            raise Exception(f"Не удалось найти или нажать кнопку 'Войти' в хедере: {str(e)}")

        # 3. Проверка открытия модалки авторизации
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    "div.side-panel-container"
                ))
            )
            take_screenshot(driver, "04_auth_modal_opened", screenshots_dir)
        except Exception as e:
            raise Exception(f"Модалка авторизации не открылась: {str(e)}")

        # 4. Вызов функции авторизации
        login_user(driver, user_type="user")
        
        # 5. Проверка успешной авторизации
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((
                    By.TAG_NAME,
                    "app-sammagonka-banner-main-page"
                ))
            )
            take_screenshot(driver, "05_after_successful_login", screenshots_dir)
        except Exception as e:
            raise Exception(f"Не удалось подтвердить успешную авторизацию: {str(e)}")

    except Exception as e:
        take_screenshot(driver, "error_"+str(e.__class__.__name__), screenshots_dir)
        pytest.fail(f"Login test failed: {str(e)}")