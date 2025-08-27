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
from home_page import get_home_url


def get_dealers_urls(driver):
    _, driver = get_home_url(url)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.scr-link.SellerInfo_link__uUN4f'))
    )
    buttons = driver.find_elements(By.CSS_SELECTOR, 'a.scr-link.SellerInfo_link__uUN4f')
    dealer_urls = []
    main_window = driver.current_window_handle

    for button in buttons:
        # Scroll to the button to ensure it's visible
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(0.5)  # Give time for scroll animation
        # Open link in new tab (COMMAND for Mac)
        ActionChains(driver).key_down(Keys.COMMAND).click(button).key_up(Keys.COMMAND).perform()
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)  # Wait for page to load
        dealer_urls.append(driver.current_url)
        driver.close()
        driver.switch_to.window(main_window)

    driver.quit()
    return dealer_urls


if __name__ == '__main__':
    start = datetime.now()
    url = 'https://www.autoscout24.com/'
    print(get_dealers_urls(url))
    end = datetime.now()
    print('Total time :', end - start)
