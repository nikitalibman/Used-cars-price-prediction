from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random_ip_agent
import time


def main(url, ua):
    chrome_options = Options()
    #ua = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"
    proxy = '20.210.113.32:80'
    chrome_options.add_argument(f'--user-agent={ua}')
    chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_driver = webdriver.Chrome(options=chrome_options)
    chrome_driver.get(url)
    page_html = chrome_driver.page_source  # Get the HTML content of the page
    chrome_driver.quit()  # Close the Chrome driver
    return page_html


if __name__ == "__main__":
    #url = 'https://www.autoscout24.com/'
    url = 'https://www.whatsmyua.info/'
    proxy, ua = random_ip_agent.rand()
    print(ua)
    page_content = main(url, ua)
    print(page_content)
