"""
This module scraps all marks names and save it into a list.
"""
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def all_marks(url):
    chrome_options = Options()
    chrome_options.add_argument('--incognito')  # Run Chrome in incognito mode
    #chrome_options.add_argument('--headless')  # Run Chrome without opening the browser')
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

    def decline_cookies():
        try:
            # Wait for the cookies consent popup to appear
            privacy_settings = chrome_driver.find_element(By.CLASS_NAME, "_consent-settings_p8dbx_100")
            if privacy_settings.is_displayed():
                # Click the "Privacy Settings" button
                privacy_settings.click()
                save_exit_button = (By.CSS_SELECTOR, 'button[data-testid="as24-cmp-accept-partial-button"]')
                save_exit_button = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable(save_exit_button))
                save_exit_button.click()
                time.sleep(2)
        except:
            pass

    decline_cookies()

    #chrome_driver.get_screenshot_as_file('screenshot.png')  # Take a screenshot

    # Wait for the marks button to be clickable
    marks_button = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'input-wrapper')))
    marks_button.click()

    wait = WebDriverWait(chrome_driver, 10)
    marks_menu = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'suggestion-item')))

    marks_list = []

    for mark in marks_menu:
        marks_list.append(mark.text)

    chrome_driver.quit()

    return marks_list


if __name__ == "__main__":
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    print(all_marks(url))