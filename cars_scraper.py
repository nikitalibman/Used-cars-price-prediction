"""
This module contains several other modules: main_pages, parsing, dataframe and sql_db. This script parses one of the
main pages in order to find all the buttons '+ Show more vehicles'. Once a link to a car dealer is clicked the module
starts to parse info about all corresponding cars. This module can be iterated over the all main pages. The result is
a table of all cars with their complete info that is exported to a SQL database. However, it takes around 1,5 hour
to complete this module.
"""
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import main_pages
import parsing
import dataframe
import random_ua
import sql_db
import marks
import time


def parser(url, marks_menu, ua):
    chrome_options = Options()

    def extra_arguments(arg):
        chrome_options.add_argument(arg)
        return chrome_options

    extra_arguments('--incognito')  # Run Chrome in incognito mode
    extra_arguments('--headless')
    chrome_options.add_argument(f'--user-agent={ua}')# Run Chrome without opening the browser
    extra_arguments('--blink-settings=imagesEnabled=false')  # Disable images
    extra_arguments('--disable-gpu')  # Disable CSS
    extra_arguments('--disable-software-rasterizer')  # Disable CSS
    extra_arguments('--disable-dev-shm-usage')  # Disable CSS
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

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

    # Looking for buttons '+ Show more vehicles' and gather them into a beatiful_soup list object
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

        # Here we start scraping info about cars from the current car dealer

        # Get a URL of the current car dealer
        href = chrome_driver.current_url
        # Collect all pages of the current car dealer
        dealer_pages = main_pages.pages_urls(href)
        # Scrap data about each car from this dealer
        cars, characteristics, prices, locations = parsing.cars_info(dealer_pages)
        # Save gathered data into a dataframe
        df = dataframe.df_construct(marks_menu, cars, characteristics, prices, locations)
        # Export formed dataframe to a SQL database
        sql_db.connect(df, 'append')

        # Close the newly opened tab
        chrome_driver.close()
        # Switch back to the original tab
        chrome_driver.switch_to.window(chrome_driver.window_handles[0])

    # Close the WebDriver to properly clean up resources
    chrome_driver.quit()


if __name__ == "__main__":
    start = datetime.now()
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    marks_menu = marks.all_marks(url)
    ua = random_ua.main()
    dealer_cars = parser(url, marks_menu, ua)
    end = datetime.now()
    print('Total time :', end - start)


