from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from config.config_secrets import CREDENTIALS

def login_user(driver, user_type="user"):
    """
    Функция для авторизации пользователя через Selenium
    :param driver: экземпляр WebDriver
    :param user_type: тип пользователя ('user' или 'admin')
    :return: None
    """
    try:
        # Получаем credentials
        credentials = CREDENTIALS[user_type]
        login = credentials["login"]
        password = credentials["password"]

        # 1. Заполнение поля логина
        try:
            login_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    "input.regular-16.input[type='text']"
                ))
            )
            login_input.clear()
            login_input.send_keys(login)
        except Exception as e:
            raise Exception(f"Не удалось найти или заполнить поле логина: {str(e)}")

        # 2. Заполнение поля пароля
        try:
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    "input.regular-16.input[type='password']"
                ))
            )
            password_input.clear()
            password_input.send_keys(password)
        except Exception as e:
            raise Exception(f"Не удалось найти или заполнить поле пароля: {str(e)}")

        # 3. Ожидание 3 секунды
        sleep(3)

        # 4. Нажатие на кнопку показать/скрыть пароль
        try:
            eye_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 
                    "use[xlink:href*='eye-closed-filled']"
                ))
            )
            eye_button.click()
        except Exception:
            pass  # Если кнопка не найдена, продолжаем

        # 5. Ожидание 3 секунды
        sleep(3)

        # 6. Нажатие кнопки "Войти"
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    "//button[contains(@class, 'afi-button') and contains(., 'Войти')]"
                ))
            )
            submit_button.click()
        except Exception as e:
            raise Exception(f"Не удалось найти или нажать кнопку 'Войти': {str(e)}")

        # 7. Ожидание полной загрузки страницы
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.TAG_NAME, "app-sammagonka-banner-main-page")
                )
            )
        except Exception as e:
            raise Exception(f"Не удалось дождаться загрузки страницы после авторизации: {str(e)}")

        # 8. Проверка наличия баннера
        try:
            banner = driver.find_element(By.TAG_NAME, "app-sammagonka-banner-main-page")
            if not banner.is_displayed():
                raise Exception("Баннер не отображается после авторизации")
        except Exception as e:
            raise Exception(f"Проблема с баннером после авторизации: {str(e)}")

        # 9. Финальное ожидание
        sleep(10)

    except Exception as e:
        try:
            # Делаем скриншот перед выбросом исключения
            driver.save_screenshot("auth_error.png")
        except Exception as screenshot_error:
            print(f"Не удалось сделать скриншот ошибки: {screenshot_error}")
        finally:
            raise Exception(f"Ошибка при авторизации: {str(e)}")