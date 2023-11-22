"""
This module does the same thing as the concurrent_thread_test. However, it works 2 times slower.
Execution time around 13 seconds.

This module selects a pair of each Proxy and a random User Agent values from the corresponding txt files. These files
have been created in advance by other modules (proxies.py and user_agents.py). This module iterates through entire txt
files and checks the connection with selected pairs IP+User Agent. In order to check that the connection is established
correctly, and we managed to change our initial IP and User Agent a website https://www.myip.com/ is used. To make
future parsing fast we filter the connection speed of every Proxy and keep only those which have less than 2 seconds.
The good proxies are saved into a txt file 'good_proxies.txt'.
"""

import requests
from bs4 import BeautifulSoup
import re
from random import choice
import concurrent.futures
from datetime import datetime

def get_html(url, useragent, proxy, timeout):
    r = requests.get(url, headers=useragent, proxies=proxy, timeout=timeout)
    return r.text

def get_ip(html):
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('div', attrs={'class': 'texto_1'}).text.strip()
    pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    ip = re.search(pattern, ip).group()
    user_agent = soup.find('div', attrs={'class': 'headers'}).find_next_sibling().text
    print('IP:', ip)
    print(user_agent)

def check_proxy(proxy, useragents, url, timeout):
    useragent = {'User-Agent': choice(useragents)}
    proxy_dict = {'http': 'http://' + proxy, 'https': 'http://' + proxy}
    try:
        html = get_html(url, useragent, proxy_dict, timeout)
        get_ip(html)
        return proxy  # Return the proxy if it's good
    except:
        print('Bad Proxy:', proxy)
        return None
    finally:
        print('---------------')

def main(url):
    useragents = open('user_agents.txt').read().split('\n')[:-1]
    proxies = open('proxies.txt').read().split('\n')[:-1]

    good_proxies = []
    g = 0
    b = 0

    timeout = 2  # Timeout in seconds

    # Number of my CPU cores is 4. By default, concurrent.futures.ThreadPoolExecutor() creates a number of threads equal
    # to the number of CPU cores available on my system
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(check_proxy, proxy, useragents, url, timeout) for proxy in proxies]

        for result in concurrent.futures.as_completed(results):
            if result.result():
                good_proxies.append(result.result())
                g += 1
            else:
                b += 1

    print('Total proxies:', len(proxies))
    print('Good proxies:', g)
    print('Bad proxies:', b)

    with open('good_proxies.txt', 'w') as file:
        for item in good_proxies:
            file.write(item + '\n')

if __name__ == '__main__':
    start = datetime.now()
    url = 'https://www.myip.com/'
    main(url)
    end = datetime.now()
    print('Total time :', end - start)

