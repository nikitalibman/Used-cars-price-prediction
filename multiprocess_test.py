

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import concurrent.futures
import random_ua
import main_pages
import parsing
import dataframe
import sql_db
import marks
import threading

def decline_cookies(driver):
    try:
        privacy_settings = driver.find_element(By.CLASS_NAME, "_consent-settings_p8dbx_100")
        if privacy_settings.is_displayed():
            privacy_settings.click()
            save_exit_button = (By.CSS_SELECTOR, 'button[data-testid="as24-cmp-accept-partial-button"]')
            save_exit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(save_exit_button))
            save_exit_button.click()
            time.sleep(2)
    except:
        pass

def parser(ua, url):
    chrome_options = Options()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(f'--user-agent={ua}')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    chrome_driver = webdriver.Chrome(options=chrome_options)

    chrome_driver.get(url)

    decline_cookies(chrome_driver)

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

def process_buttons(ua, buttons):
    threads = []
    for button in buttons:
        url = button.get_attribute('href')
        thread = threading.Thread(target=parser, args=(ua, url))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start = datetime.now()
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    marks_menu = marks.all_marks(url)
    ua = random_ua.main()

    chrome_options = Options()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(f'--user-agent={ua}')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    chrome_driver = webdriver.Chrome(options=chrome_options)
    chrome_driver.get(url)

    decline_cookies(chrome_driver)

    buttons = chrome_driver.find_elements(By.LINK_TEXT, '+ Show more vehicles')

    # Use threading to parallelize the parser function
    process_buttons(ua, buttons)

    chrome_driver.quit()

    end = datetime.now()
    print('Total time:', end - start)

