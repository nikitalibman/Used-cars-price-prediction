"""
This module declines cookies when enter the autoscout website.
"""
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def decline_cookies(chrome_driver: webdriver.Chrome) -> None:
    """Wait for the cookies consent popup window to appear and then decline cookies."""

    privacy_settings = chrome_driver.find_element(By.CLASS_NAME, "_consent-settings_1lphq_103")
    if privacy_settings.is_displayed():
        # Click the "Privacy Settings" button
        privacy_settings.click()
        save_exit_button = (By.CSS_SELECTOR, 'button[data-testid="as24-cmp-accept-partial-button"]')
        save_exit_button = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable(save_exit_button))
        save_exit_button.click()
        time.sleep(2)


def get_url(url: str) -> tuple[webdriver.Chrome, str]:
    """Get URL of the current page."""
    
    chrome_options = Options()
    chrome_options.add_argument('--incognito')  # Run Chrome in incognito mode
    chrome_options.add_argument('--headless')  # Run Chrome without opening the browser')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images
    chrome_options.add_argument('--disable-gpu')  # Disable CSS
    chrome_options.add_argument('--disable-software-rasterizer')  # Disable CSS
    chrome_options.add_argument('--disable-dev-shm-usage')  # Disable CSS
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) # Disable automation flags
    chrome_options.add_experimental_option('useAutomationExtension', False) # Disable automation flags
    chrome_driver = webdriver.Chrome(options=chrome_options)
    # Get the page content
    chrome_driver.get(url)

    decline_cookies(chrome_driver)

    current_url = chrome_driver.current_url

    return chrome_driver, current_url


if __name__ == "__main__":
    url = 'https://www.autoscout24.com/'
    driver, url_result = get_url(url)
    driver.quit()
    print(url_result)
    print(driver)
