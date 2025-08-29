"""
This script parses one of the main pages in order to find all the buttons '+ Show more vehicles'. Once the button is
found it is clicked and a page opens in a new tab. Then a URL of the current page is acquired and stored into a list.
The output of the script is a list of all acquired dealers links from the current main page.
Execution time is 1 minute and 6 seconds.
"""

from datetime import datetime
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from main_pages import total_pages
from bs4 import BeautifulSoup
from home_page import get_home_url


def get_dealers_urls(url):
    _, driver = get_home_url(url)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.scr-link.SellerInfo_link__uUN4f'))
    )
    buttons = driver.find_elements(By.CSS_SELECTOR, 'a.scr-link.SellerInfo_link__uUN4f')
    dealer_urls = []
    pages = []
    main_window = driver.current_window_handle

    for button in buttons:
        # Scroll to the button to ensure it's visible
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(0.5)   # Give time for scroll animation
        # Open link in new tab (COMMAND for Mac)
        ActionChains(driver).key_down(Keys.COMMAND).click(button).key_up(Keys.COMMAND).perform()
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)  # Wait for page to load
        # Find and click the first Dealer's page in the pagination on the bottom of the page
        dealer_first_page = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Go to page 1']")))
        dealer_first_page.click()
        time.sleep(2)
        dealer_urls.append(driver.current_url)
        html = requests.get(driver.current_url).text
        soup = BeautifulSoup(html, 'lxml')
        pages.append(total_pages(soup))
        # dealer_urls = driver.current_url
        driver.close()
        driver.switch_to.window(main_window)

    # Create dictionary mapping dealer URL to number of pages
    dealer_pages_dict = dict(zip(dealer_urls, pages))
    driver.quit()
    return dealer_pages_dict


if __name__ == '__main__':
    start = datetime.now()
    url = 'https://www.autoscout24.com/'
    print(get_dealers_urls(url))
    end = datetime.now()
    print('Total time :', end - start)
