"""
The script scraps information about all dealers' cars.
It parses the main page in order to find all the buttons '+ Show more vehicles'. Once the button is
found it is clicked and a page opens in a new tab. Then a URL of the current page is acquired and stored into a list.
An algorithm of the module 'main_page_parsing_flow.py' is used to parse cars' info and then upload it to Postgres database.
"""
import time
import requests
from datetime import datetime
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from main_page_parsing_flow import total_pages, get_home_url, load_to_postgres


def get_main_dealers_urls(autoscout_url: str) -> dict:
    """Collect all dealers' main URLs and total number of pages into a dictionary."""

    _, driver = get_home_url(autoscout_url)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'a.scr-link.SellerInfo_link__uUN4f'))
    )
    buttons = driver.find_elements(
        By.CSS_SELECTOR, 'a.scr-link.SellerInfo_link__uUN4f')
    dealer_urls = []
    pages = []
    main_window = driver.current_window_handle

    for button in buttons:
        # Scroll to the button to ensure it's visible
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(0.5)   # Give time for scroll animation
        # Open link in a new tab (COMMAND for Mac)
        ActionChains(driver).key_down(Keys.COMMAND).click(
            button).key_up(Keys.COMMAND).perform()
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)  # Wait for page to load
        # Find and click the first Dealer's page in the pagination on the bottom of the page
        dealer_first_page = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Go to page 1']")))
        dealer_first_page.click()
        time.sleep(2)
        dealer_urls.append(driver.current_url)
        html = requests.get(driver.current_url).text
        soup = BeautifulSoup(html, 'lxml')
        pages.append(total_pages(soup))
        driver.close()
        driver.switch_to.window(main_window)

    # Create dictionary mapping dealer URL to number of pages
    dealer_pages_dict = dict(zip(dealer_urls, pages))

    return dealer_pages_dict


def get_suburls(autoscout_url: str) -> tuple[list, list]:
    """Construct every dealer's sub URL with a certain page number."""

    dealer_pages_dict = get_main_dealers_urls(autoscout_url)
    all_urls = []
    print('List of dealers:')
    for dealer in dealer_pages_dict.items():
        cid = list(dealer)[0].split('cid=')[1].split('&')[0]
        url_before_page_number = list(dealer)[0].split('page=')[0]
        after = list(dealer)[0].split('page=')[1].split('&')[1]
        print(
            f'Dealer \033[1m{cid}\033[0m has - \033[1m{list(dealer)[1]}\033[0m page(s).')
        all_pages = list(dealer)[1]
        for page in range(1, all_pages + 1):
            whole = f'{url_before_page_number}page={page}&{after}'
            all_urls.append(whole)

    return all_urls, all_pages


def get_all_dealers_cars(autoscout_url: str) -> load_to_postgres:
    """Form a dataframe of every dealer and upload it to Postgres database."""
    all_urls, all_pages = get_suburls(autoscout_url)
    for dealer_url in all_urls:
        cid = dealer_url.split('cid=')[1].split('&')[0]
        page = dealer_url.split('page=')[1].split('&')[0]
        print(
            f'Parsing page number \033[1m{page}\033[0m out of \033[1m{all_pages}\033[0m from the dealer \033[1m{cid}\033[0m.')
        print('Loading data to the database')
        load_to_postgres(autoscout_url, param='append')
        print('----------------')


if __name__ == '__main__':
    print('Script execution is started.')
    start = datetime.now()
    autoscout_url = 'https://www.autoscout24.com/'
    get_all_dealers_cars(autoscout_url)
    end = datetime.now()
    print('Total time :', end - start)
