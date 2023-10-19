"""
This module randomly selects a pair of IP and User Agent values from the corresponding txt files. These files have been
created in advance by other modules (proxies.py and user_agents.py). This module iterates through entire txt files and
checks the connection with randomly selected pairs IP+User Agent. In order to check that the connection is established
correctly, and we managed to change our initial IP and User Agent a website https://www.myip.com/ is used.
"""

import requests
from bs4 import BeautifulSoup
import re
from random import choice


def get_html(url, useragent, proxy):
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text


def get_ip(html):
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('div', attrs={'class': 'texto_1'}).text.strip()
    pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    ip = re.search(pattern, ip).group()
    user_agent = soup.find('div', attrs={'class': 'headers'}).find_next_sibling().text
    print('IP:', ip)
    print(user_agent)
    print('---------------')


def main():
    useragents = open('user_agents.txt').read().split('\n')
    proxies = open('proxies.txt').read().split('\n')

    for i in range(10):
        # sleep(uniform(3, 6))
        proxy = {'http': 'http://' + choice(proxies),
                 "https": 'http://' + choice(proxies)}
        useragent = {'User-Agent': choice(useragents)}
        try:
            html = get_html(url, useragent, proxy)
        except:
            continue
        get_ip(html)


if __name__ == '__main__':
    url = 'https://www.myip.com/'
    main()
