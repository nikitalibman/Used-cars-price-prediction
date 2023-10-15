from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


def sel_pars(url):
    chrome_options = Options()

    def extra_arguments(arg):
        chrome_options.add_argument(arg)
        return chrome_options

    extra_arguments('--incognito')  # Run Chrome in incognito mode
    extra_arguments('--headless')  # Run Chrome without opening the browser')
    extra_arguments('--blink-settings=imagesEnabled=false')  # Disable images
    extra_arguments('--disable-gpu')  # Disable CSS
    extra_arguments('--disable-software-rasterizer')  # Disable CSS
    extra_arguments('--disable-dev-shm-usage')  # Disable CSS

    chrome_driver = webdriver.Chrome(options=chrome_options)

    # Set Chrome preferences to automatically accept cookies
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})

    # Get the page content
    chrome_driver.get(url)

    def cookies_accept():
        try:
            # Wait for the consent popup to appear
            consent_popup = WebDriverWait(chrome_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, '_consent-popup_1i5cd_1'))
            )
            # Check if the "Accept All" button is present
            accept_all_button = consent_popup.find_element(By.XPATH, '//button[@class="_consent-accept_1i5cd_111"]')
            if accept_all_button.is_displayed():
                # Click the "Accept All" button
                accept_all_button.click()

                # Wait for the consent popup to disappear (short timeout)
                WebDriverWait(chrome_driver, 10).until_not(
                    EC.presence_of_element_located((By.CLASS_NAME, '_consent-popup_1i5cd_1'))
                )
        except:
            pass

    cookies_accept()

    dealer_cars = []

    buttons = chrome_driver.find_elements(By.LINK_TEXT, '+ Show more vehicles')

    for button in buttons:
        # Open the link in a new tab
        ActionChains(chrome_driver).key_down(Keys.CONTROL).click(button).key_up(Keys.CONTROL).perform()
        # Wait for the new tab to appear
        WebDriverWait(chrome_driver, 15).until(lambda driver: len(chrome_driver.window_handles) > 1)
        # Switch to the newly opened tab
        chrome_driver.switch_to.window(chrome_driver.window_handles[-1])
        # Add a delay to ensure the new tab is fully loaded
        time.sleep(5)
        # Append the new tab's URL to the 'dealer_cars' list
        dealer_cars.append(chrome_driver.current_url)
        # Close the newly opened tab
        chrome_driver.close()
        # Switch back to the original tab
        chrome_driver.switch_to.window(chrome_driver.window_handles[0])

    # Close the WebDriver to properly clean up resources
    chrome_driver.quit()

    return dealer_cars


if __name__ == "__main__":
    dealer_cars = sel_pars()

    # 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU')

