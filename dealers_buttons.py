"""
This script parses one of the main pages in order to find all the buttons '+ Show more vehicles'. Once the button is
found it is clicked and a page opens in a new tab. Then a URL of the current page is acquired and stored into a list.
The output of the script is a list of all acquired dealers links from the current main page.
Execution time is 1 minute and 6 seconds.
"""

from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random_ua
import time


def chrome_options():
    chrome_options = Options()
    chrome_options.add_argument('--incognito')  # Run Chrome in incognito mode
    chrome_options.add_argument('--headless')  # Run Chrome without opening the browser
    chrome_options.add_argument(f'--user-agent={random_ua.main()["User-Agent"]}')  # change user agent
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images
    chrome_options.add_argument('--disable-gpu')  # Disable CSS
    chrome_options.add_argument('--disable-software-rasterizer')  # Disable CSS
    chrome_options.add_argument('--disable-dev-shm-usage')  # Disable CSS
    chrome_options.add_argument('--window-size=1920,1080')  # set custom screen resolution
    chrome_options.add_experimental_option("excludeSwitches",
                                           ["enable-automation"])  # Avoid automated testing detection
    chrome_options.add_experimental_option('useAutomationExtension', False)  # Turn off detection as an automated script
    return chrome_options


def decline_cookies(chrome_driver):
    try:
        # Wait for the cookies consent popup to appear
        privacy_settings = chrome_driver.find_element(By.CLASS_NAME, "_consent-settings_p8dbx_100")
        if privacy_settings.is_displayed():
            # Click the "Privacy Settings" button
            privacy_settings.click()
            save_exit_button = (By.CSS_SELECTOR, 'button[data-testid="as24-cmp-accept-partial-button"]')
            save_exit_button = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable(save_exit_button))
            save_exit_button.click()
    except Exception as ex:
        print(ex)


def find_buttons(chrome_driver):
    # Looking for buttons '+ Show more vehicles' and gather them into a beatiful_soup list object
    buttons = chrome_driver.find_elements(By.LINK_TEXT, '+ Show more vehicles')
    return buttons


def button_click(chrome_driver, button):
    # Here we pick a random User Agent
    user_agent = random_ua.main()
    # Set the user agent for the current tab
    chrome_driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent['User-Agent']})
    # Open the link in a new tab
    ActionChains(chrome_driver).key_down(Keys.CONTROL).click(button).key_up(Keys.CONTROL).perform()
    # Wait for the new tab to appear
    WebDriverWait(chrome_driver, 15).until(lambda driver: len(chrome_driver.window_handles) > 1)
    # Switch to the newly opened tab
    chrome_driver.switch_to.window(chrome_driver.window_handles[-1])
    # Add a delay to ensure the new tab is fully loaded
    time.sleep(1)
    href = chrome_driver.current_url
    # Close the newly opened tab
    chrome_driver.close()
    # Switch back to the original tab
    chrome_driver.switch_to.window(chrome_driver.window_handles[0])
    return href


def main(url):
    options = chrome_options()
    chrome_driver = webdriver.Chrome(options=options)
    chrome_driver.get(url)
    decline_cookies(chrome_driver)
    time.sleep(1)
    buttons = find_buttons(chrome_driver)
    hrefs = []
    for button in buttons:
        hrefs.append(button_click(chrome_driver, button))
    chrome_driver.quit()
    return hrefs


if __name__ == '__main__':
    start = datetime.now()
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    print(main(url))
    end = datetime.now()
    print('Total time :', end - start)

