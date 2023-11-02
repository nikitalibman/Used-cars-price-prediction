from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random_ip_agent
import time


def main(url, proxy, useragent):
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_options.add_argument(f'--user-agent={useragent}')
    chrome_options.add_argument('--incognito') # Run Chrome in incognito mode
    # extra_arguments(chrome_options, '--headless')  # Run Chrome without opening the browser')
    # extra_arguments(chrome_options, '--blink-settings=imagesEnabled=false')  # Disable images
    # extra_arguments(chrome_options, '--disable-gpu')  # Disable CSS
    # extra_arguments(chrome_options, '--disable-software-rasterizer')  # Disable CSS
    # extra_arguments(chrome_options, '--disable-dev-shm-usage')  # Disable CSS

    chrome_driver = webdriver.Chrome(options=chrome_options)

    # Set Chrome preferences to automatically accept cookies
    # chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})

    # Get the page content
    chrome_driver.get(url)

    time.sleep(5)

    chrome_driver.quit()


if __name__ == "__main__":
    #url = 'https://www.myip.com/'
    url = 'http://www.whatismyproxy.com/'
    #url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    proxy, useragent = random_ip_agent.rand()
    print(proxy)
    print(useragent)
    main(url, proxy, useragent)
