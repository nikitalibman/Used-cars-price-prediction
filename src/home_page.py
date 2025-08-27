from decline_cookies import get_url
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_home_url(url):
    """Load the home autoscout page and click on the button 'Results'."""
    chrome_driver, current_url = get_url(url)
    # Wait for the 'results' button to be clickable
    results_button = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.ID, 'search-mask-search-cta')))
    results_button.click()

    wait = WebDriverWait(chrome_driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ListItem_title_bold__iQJRq')))

    current_url = chrome_driver.current_url

    return current_url, chrome_driver


if __name__ == '__main__':
    url = 'https://www.autoscout24.com/'
    which_url, driver = get_home_url(url)
    driver.quit()
    print(which_url)
    print(driver)
