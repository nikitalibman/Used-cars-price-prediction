import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.autoscout24.com/lst?atype=C&desc=0&page=1&search_id=7ka6orz363&sort=standard&source=listpage_pagination&ustate=N%2CU'
html = requests.get(url).text

# Set up Chrome options for a headless browser
chrome_options = Options()
#chrome_options.add_argument('--headless')  # Run Chrome in headless mode
#chrome_options.add_argument('--incognito')
chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
chrome_driver = webdriver.Chrome(options=chrome_options)
#try:
    # Get the page content
chrome_driver.get(url)
WebDriverWait(chrome_driver, 40).until(
    EC.invisibility_of_element_located((By.ID, 'as24-cmp-popup'))
)
link = chrome_driver.find_element(By.LINK_TEXT, '+ Show more vehicles')
link.click()
#finally:
#print(chrome_driver.page_source)
while True:
    pass
    #chrome_driver.quit()
