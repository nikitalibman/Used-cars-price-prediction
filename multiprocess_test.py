"""
This module parses info from one of the main pages. It looks for the buttons '+ Show more vehicles' and cliscks on them.
Once a link to a car dealer is clicked the module starts to parse info about all corresponding cars. This module
contains several other modules: main_pages, parsing, dataframe and sql_db.  However, it takes around 1,5 hour to
complete this module. In order to speed this script a multithreading approach is implemented. Clicking on the car
dealers buttons with further info scraping will be split into several concurrent threads.

"""

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
import sql_db
import marks
import time
import random_ip_agent
import concurrent.futures


def parser(url, marks_menu, ua):

    chrome_options = Options()
    chrome_options.add_argument('--incognito')  # Run Chrome in incognito mode
    #chrome_options.add_argument('--headless')  # Run Chrome without opening the browser')
    chrome_options.add_argument(f'--user-agent={ua}') # Change User Agent
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images
    chrome_options.add_argument('--disable-gpu')  # Disable CSS
    chrome_options.add_argument('--disable-software-rasterizer')  # Disable CSS
    chrome_options.add_argument('--disable-dev-shm-usage')  # Disable CSS
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

    # Looking for buttons '+ Show more vehicles' and gather them into a beatiful_soup list object
    buttons = chrome_driver.find_elements(By.LINK_TEXT, '+ Show more vehicles')


    def button_clicker():

        for button in buttons:

            chrome_driver = webdriver.Chrome(options=chrome_options)
            # Here we pick a random User Agent
            proxy, user_agent = random_ip_agent.rand()
            # Set the user agent for the current tab
            chrome_driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent['User-Agent']})
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

    button_clicker()

    # Here we start the multi threading. The buttons '+ Show more vehicles' will be clicked simultaneously.
    #with concurrent.futures.ThreadPoolExecutor() as executor:
    #    results = [executor.submit(button_clicker, button) for button in buttons]

if __name__ == "__main__":
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    marks_menu = marks.all_marks(url)
    proxy, ua = random_ip_agent.rand()
    dealer_cars = parser(url, marks_menu, ua)
