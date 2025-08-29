from dealers_urls import get_dealers_urls
from main_pages import total_pages
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

url = 'https://www.autoscout24.com/'    
dealer_urls, chrome_driver = get_dealers_urls(url)
html = requests.get(dealer_urls[0]).text
soup = BeautifulSoup(html, 'lxml')
result = total_pages(soup) 
dealer_first_page = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Go to page 1']")))
dealer_first_page.click()
time.sleep(0.5)
current_url = chrome_driver.current_url
chrome_driver.quit()

print('First dealer')
print('####################')
print(dealer_urls)
print('Number of pages')
print('####################')
print(result)
print('####################')
print("Current URL of the 1st Dealer's pag.")
print(current_url)