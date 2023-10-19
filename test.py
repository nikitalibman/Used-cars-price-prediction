"""
This module goes around each main page and clicks on hyper links under every car description. This link takes us
to the dealer of this car and all other cars that belong to him. The structure is the same as with the main pages.
The main goal is to obtain URL links to all these dealers.
"""

from multiprocessing import Pool, Manager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random_ip_agent


def extra_arguments(chrome_options, arg):
    chrome_options.add_argument(arg)
    return chrome_options


def cookies_accept(chrome_driver):
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


def click_button(buttons, chrome_driver, dealer_cars):
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


def main(url, proxy, useragent):
    chrome_options = Options()
    extra_arguments(chrome_options, f'--proxy-server={proxy}')
    extra_arguments(chrome_options, f'--user-agent={useragent}')
    extra_arguments(chrome_options, '--incognito')  # Run Chrome in incognito mode
    extra_arguments(chrome_options, '--headless')  # Run Chrome without opening the browser')
    extra_arguments(chrome_options, '--blink-settings=imagesEnabled=false')  # Disable images
    extra_arguments(chrome_options, '--disable-gpu')  # Disable CSS
    extra_arguments(chrome_options, '--disable-software-rasterizer')  # Disable CSS
    extra_arguments(chrome_options, '--disable-dev-shm-usage')  # Disable CSS

    chrome_driver = webdriver.Chrome(options=chrome_options)

    # Set Chrome preferences to automatically accept cookies
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})

    # Get the page content
    chrome_driver.get(url)

    cookies_accept(chrome_driver)
    manager = Manager()
    dealer_cars = manager.list()  # Create a shared list

    #dealer_cars = []

    buttons = chrome_driver.find_elements(By.LINK_TEXT, '+ Show more vehicles')

    with Pool(10) as p:
        #p.map(click_button, buttons)
        p.starmap(click_button, [(button, chrome_driver, dealer_cars) for button in buttons])

    # Close the WebDriver to properly clean up resources
    chrome_driver.quit()
    return list(dealer_cars)


if __name__ == "__main__":
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    proxy, useragent = random_ip_agent.rand()
    dealer_cars = main(url, proxy, useragent)
    print(dealer_cars)
