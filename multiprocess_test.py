

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
    chrome_options = Options()
    chrome_options.add_argument('--incognito')
    #chrome_options.add_argument('--headless')  # Run Chrome without opening the browser'
    chrome_options.add_argument(f'--user-agent={random_ua.main()["User-Agent"]}')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    chrome_driver = webdriver.Chrome(options=chrome_options)
    try:
        current_tab_handle = chrome_driver.current_window_handle
        # Get the page content
        chrome_driver.get(url)

        # Decline cookies if the popup is present
        decline_cookies(chrome_driver)

        # Here we pick a random User Agent
        user_agent = random_ua.main()
        # Set the user agent for the current tab
        chrome_driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent['User-Agent']})
        # Open the link in a new tab
        #ActionChains(chrome_driver).key_down(Keys.CONTROL).click(button).key_up(Keys.CONTROL).perform()
        # Open the link in a new tab using JavaScript to simulate a click
        chrome_driver.execute_script("arguments[0].target='_blank'; arguments[0].click();", button)
        # Wait for the new tab to appear
        WebDriverWait(chrome_driver, 15).until(lambda driver: len(chrome_driver.window_handles) > 1)
        # Identify the new tab handle
        new_tab_handle = [handle for handle in chrome_driver.window_handles if handle != current_tab_handle][0]
        # Switch to the newly opened tab
        chrome_driver.switch_to.window(new_tab_handle)
        #chrome_driver.switch_to.window(chrome_driver.window_handles[-1])
        # Wait for an element with the specified class to be present on the page
        element_class = "ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l"
        WebDriverWait(chrome_driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, element_class)))
        # Add a delay to ensure the new tab is fully loaded
        #time.sleep(5)

        # Here we start scraping info about cars from the current car dealer
        # Get a URL of the current car dealer
        href = chrome_driver.current_url
        # Collect all pages of the current car dealer
        dealer_pages = main_pages.pages_urls(href)
        # Scrap data about each car from this dealer
        cars, characteristics, prices, locations = parsing.cars_info(dealer_pages)
        # Save gathered data into a dataframe
        df = dataframe.df_construct(marks_menu, cars, characteristics, prices, locations)
        print(df)
        # Export formed dataframe to a SQL database
        sql_db.connect(df, 'append')
        print(f'Data exported from the dealer {button}')
    finally:
        # Close the WebDriver to properly clean up resources
        chrome_driver.quit()

def main(url, marks_menu, ua):
    chrome_options = Options()
    chrome_options.add_argument('--incognito')
    #chrome_options.add_argument('--headless')  # Run Chrome without opening the browser'
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
    print('start of multithreading')
    # Here we start the multi-threading. The buttons '+ Show more vehicles' will be clicked simultaneously.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(button_clicker, button, marks_menu) for button in buttons]

    # Wait for all threads to complete
    concurrent.futures.wait(futures)

    # Close the WebDriver to properly clean up resources
    chrome_driver.quit()

if __name__ == "__main__":
    start = datetime.now()
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    marks_menu = marks.all_marks(url)
    ua = random_ua.main()
    main(url, marks_menu, ua)
    end = datetime.now()
    print('Total time :', end - start)

