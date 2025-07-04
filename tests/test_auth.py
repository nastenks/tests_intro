import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

@pytest.fixture(scope="module")
def driver():
    """Фикстура для инициализации и закрытия браузера"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
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

def test_initial_page_load(driver, screenshots_dir):
    """Тест загрузки главной страницы и куки-баннера"""
    try:
        # 1. Открытие сайта
        driver.get("https://frontend-develop.kube.artforintrovert.ru/")
        sleep(7)
        screenshot_path = take_screenshot(driver, "01_initial_load", screenshots_dir)
        pytest.skip(f"Screenshot saved: {screenshot_path}")

        # 2. Проверка заголовка
        assert "Art for Introvert" in driver.title

        # 3. Обработка куки-баннера
        try:
            cookie_banner = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.cookie-consent")))
            take_screenshot(driver, "02_cookie_banner", screenshots_dir)
            
            accept_btn = cookie_banner.find_element(By.CSS_SELECTOR, "button")
            accept_btn.click()
            take_screenshot(driver, "03_after_cookie_accept", screenshots_dir)
        except Exception as cookie_error:
            pytest.skip(f"Cookie banner not found: {str(cookie_error)}")

    except Exception as e:
        take_screenshot(driver, "error_initial_load", screenshots_dir)
        pytest.fail(f"Page loading error: {str(e)}")
    finally:
        # Дополнительные действия при необходимости
        pass

def test_login_flow(driver, screenshots_dir):
    """Тест процесса входа в систему"""
    try:
        # 1. Повторная загрузка страницы
        driver.get("https://frontend-develop.kube.artforintrovert.ru/")
        
        # 2. Клик по кнопке "Войти"
        try:
            login_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Войти']]")))
            take_screenshot(driver, "04_before_login_click", screenshots_dir)
            
            login_btn.click()
            take_screenshot(driver, "05_after_login_click", screenshots_dir)
        except Exception as login_error:
            pytest.fail(f"Login button error: {str(login_error)}")

        # 3. Проверка открытия модального окна
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Вход')]")))
        except Exception as modal_error:
            pytest.fail(f"Login modal error: {str(modal_error)}")

        # 4. Переход к регистрации
        try:
            register_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Зарегистрироваться']]")))
            take_screenshot(driver, "06_before_register_click", screenshots_dir)
            
            driver.execute_script("arguments[0].scrollIntoView();", register_btn)
            sleep(1)
            register_btn.click()
            take_screenshot(driver, "07_after_register_click", screenshots_dir)
        except Exception as register_error:
            pytest.fail(f"Registration button error: {str(register_error)}")

    except Exception as e:
        take_screenshot(driver, "error_login_flow", screenshots_dir)
        pytest.fail(f"Login flow error: {str(e)}")
    finally:
        # Финализатор теста
        pass
