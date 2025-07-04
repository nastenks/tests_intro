# /utils/selenium_utils.py
import os
from datetime import datetime
from selenium import webdriver

SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def init_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    return driver

def take_screenshot(driver, name=""):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{name}.png" if name else f"{timestamp}.png"
    path = os.path.join(SCREENSHOTS_DIR, filename)
    driver.save_screenshot(path)
    print(f"📸 Скриншот сохранён: {path}")
    return path