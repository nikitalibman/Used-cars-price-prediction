"""
This module creates a list of most common User Agents. In order to form this list we parse a website
https://techblog.willshouse.com/2012/01/03/most-common-user-agents/. The result of this module is a txt file
'user_agents.txt' with a comprehensive list of User Agents.
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def main(url):
    chrome_driver = webdriver.Chrome()
    chrome_driver.get(url)

    user_agents = []

    elements = WebDriverWait(chrome_driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,
                                                                                           'useragent')))
    for element in elements:
        user_agents.append(element.text)

        with open('user_agents.txt', 'w') as f:
            for item in user_agents[1:]:
                f.write("%s\n" % item)

if __name__ == '__main__':
    url = 'https://techblog.willshouse.com/2012/01/03/most-common-user-agents/'
    main(url)
