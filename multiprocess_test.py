

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
import random_ip_agent
import main_pages
import parsing
import dataframe
import sql_db
import marks
import threading


lock = threading.Lock()


def decline_cookies(driver):
    try:
        # Wait for the cookies consent popup to appear
        privacy_settings = driver.find_element(By.CLASS_NAME, "_consent-settings_p8dbx_100")
        if privacy_settings.is_displayed():
            # Click the "Privacy Settings" button
            privacy_settings.click()
            save_exit_button = (By.CSS_SELECTOR, 'button[data-testid="as24-cmp-accept-partial-button"]')
            save_exit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(save_exit_button))
            save_exit_button.click()
            time.sleep(2)
    except:
        pass

def button_clicker(button, marks_menu):
    # Create a new WebDriver instance for each thread
    chrome_options = Options()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless')  # Run Chrome without opening the browser
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    with webdriver.Chrome(options=chrome_options) as chrome_driver:
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

        try:
            #with lock:
            #print("Inside the lock")
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
            print(f'Data exported from the dealer {button}')

        except Exception as e:
            print(f"An error occurred: {str(e)}")

def main(url, marks_menu, ua):
    chrome_options = Options()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless')  # Run Chrome without opening the browser'
    chrome_options.add_argument(f'--user-agent={ua}')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    chrome_driver = webdriver.Chrome(options=chrome_options)

    # Get the page content
    chrome_driver.get(url)

    # Decline cookies if the popup is present
    decline_cookies(chrome_driver)

    # Looking for buttons '+ Show more vehicles' and gather them into a beautiful_soup list object
    buttons = WebDriverWait(chrome_driver, 15).until(
        EC.presence_of_all_elements_located((By.LINK_TEXT, '+ Show more vehicles'))
    )

    # Here we start the multi-threading. The buttons '+ Show more vehicles' will be clicked simultaneously.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(button_clicker, buttons, [marks_menu] * len(buttons))

    # Close the WebDriver to properly clean up resources
    chrome_driver.quit()

if __name__ == "__main__":
    start = datetime.now()
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    marks_menu = marks.all_marks(url)
    proxy, ua = random_ip_agent.rand()
    dealer_cars = main(url, marks_menu, ua)
    end = datetime.now()
    print('Total time :', end - start)

