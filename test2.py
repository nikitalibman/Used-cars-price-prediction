from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random_ip_agent
import time


def main(url):

    chrome_driver = webdriver.Chrome()
    chrome_driver.get(url)
    page_html = chrome_driver.page_source  # Get the HTML content of the page
    #chrome_driver.quit()  # Close the Chrome driver
    return page_html


if __name__ == "__main__":
    url = 'https://www.autoscout24.com/'
    #proxy, useragent = random_ip_agent.rand()
    #print(proxy, useragent)
    dealer_cars = main(url)
    print(dealer_cars)

