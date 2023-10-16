from selenium import webdriver
import time
from selenium.webdriver.common.by import By

def scroll_down(driver, pixels):
    # Execute JavaScript to scroll down by the specified number of pixels
    driver.execute_script(f"window.scrollBy(0, {pixels});")

def main(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(2)
    scroll_down(driver, 300)
    elements = driver.find_elements(By.CLASS_NAME, 'icon')
    elements[1].click()
    elements[4].click()
    driver.find_element(By.XPATH, "//button[text()='Show']").click()
    time.sleep(15)
    driver.find_element(By.CLASS_NAME, "ctp-checkbox-label").click()
    time.sleep(15)

if __name__ == '__main__':
    url = 'https://hidemy.io/en/proxy-list/'
    main(url)
