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


def parser(url, marks_menu):
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

    # dealer_cars = []

    # Looking for buttons '+ Show more vehicles' and gather them into a beatiful_soup list object
    buttons = chrome_driver.find_elements(By.LINK_TEXT, '+ Show more vehicles')

    #i = 0

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
        #print(f'Car dealer {i} parsed:', href)
        #i += 1

        # Close the newly opened tab
        chrome_driver.close()
        # Switch back to the original tab
        chrome_driver.switch_to.window(chrome_driver.window_handles[0])

    # Close the WebDriver to properly clean up resources
    chrome_driver.quit()

    # return dealer_cars


if __name__ == "__main__":
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    marks_menu = marks.all_marks(url)
    dealer_cars = parser(url, marks_menu)
