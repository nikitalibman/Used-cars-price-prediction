"""
This module scraps all marks names and save it into a list.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def all_marks(url):
    chrome_options = Options()
    chrome_options.add_argument('--incognito')  # Run Chrome in incognito mode
    chrome_options.add_argument('--headless')  # Run Chrome without opening the browser')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images
    chrome_options.add_argument('--disable-gpu')  # Disable CSS
    chrome_options.add_argument('--disable-software-rasterizer')  # Disable CSS
    chrome_options.add_argument('--disable-dev-shm-usage')  # Disable CSS
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_driver = webdriver.Chrome(options=chrome_options)

    # Set Chrome preferences to automatically accept cookies
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})

    # Get the page content
    chrome_driver.get(url)

    def cookies_accept():
        try:
            # Wait for the consent popup to appear
            consent_popup = WebDriverWait(chrome_driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, '_consent-popup_1i5cd_1'))
            )
            # Check if the "Accept All" button is present
            accept_all_button = consent_popup.find_element(By.XPATH, '//button[@class="_consent-accept_1i5cd_111"]')
            if accept_all_button.is_displayed():
                # Click the "Accept All" button
                accept_all_button.click()

                # Wait for the consent popup to disappear (short timeout)
                WebDriverWait(chrome_driver, 1).until_not(
                    EC.presence_of_element_located((By.CLASS_NAME, '_consent-popup_1i5cd_1'))
                )
        except:
            pass

    cookies_accept()

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
    print(marks_list)

    return marks_list


if __name__ == "__main__":
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    all_marks(url)