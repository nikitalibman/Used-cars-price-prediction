"""
This module creates a list of most common User Agents. In order to form this list we parse a website
https://techblog.willshouse.com/2012/01/03/most-common-user-agents/. The result of this module is a txt file
'user_agents.txt' with a comprehensive list of User Agents.
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json


def main(url):
    chrome_driver = webdriver.Chrome()
    chrome_driver.get(url)

    main_element = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'most-common-desktop-useragents-json-csv'))
    )
    nested_element = main_element.find_element(By.CLASS_NAME, 'col-lg-6')
    json_ua = nested_element.find_element(By.CLASS_NAME, 'form-control').text

    user_agents_list = json.loads(json_ua)

    user_agents = [entry['ua'] for entry in user_agents_list]

    with open('user_agents.txt', 'w') as f:
        for ua in user_agents:
            f.write(f'{ua}\n')


if __name__ == '__main__':
    url = 'https://www.useragents.me/#most-common-desktop-useragents-json-csv'
    main(url)
