import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.autoscout24.com/lst?atype=C&desc=0&page=1&search_id=7ka6orz363&sort=standard&source=listpage_pagination&ustate=N%2CU'
html = requests.get(url).text
chrome_options = Options()
chrome_options.add_argument('--incognito')
# Set Chrome preferences to automatically accept cookies
chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})

chrome_driver = webdriver.Chrome(options=chrome_options)

# Get the page content
chrome_driver.get(url)

# Wait for the consent popup to appear (short timeout)
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

# Find and click the desired element
link = chrome_driver.find_element(By.LINK_TEXT, '+ Show more vehicles')
link.click()

while True:
    pass

# Close the WebDriver to properly clean up resources
#chrome_driver.quit()
