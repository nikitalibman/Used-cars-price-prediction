"""
This module selects a pair of each Proxy and random User Agent values from the corresponding txt files. These files have
been created in advance by other modules (proxies.py and user_agents.py). This module iterates through entire txt files
and checks the connection with selected pairs IP+User Agent. In order to check that the connection is established
correctly, and we managed to change our initial IP and User Agent a website https://www.myip.com/ is used. To make
future parsing fast we filter the connection speed of every Proxy and keep only those which have less than 2 seconds.
The good proxies are saved into a txt file 'good_proxies.txt'.
"""

import requests
from bs4 import BeautifulSoup
import re
from random import choice


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


def main():
    useragents = open('user_agents.txt').read().split('\n')[:-1]
    proxies = open('proxies.txt').read().split('\n')[:-1]
    good_proxies = []
    g = 0
    b = 0
    for i in proxies:
        proxy = {'http': 'http://' + i,
                 'https': 'http://' + i}
        useragent = {'User-Agent': choice(useragents)}
        try:
            html = get_html(url, useragent, proxy,
                            timeout=2)  # Keep proxies with the connection time less than 1 second
            get_ip(html)
            good_proxies.append(i)
            g += 1
        except:
            print('Bad Proxy:', i)
            b += 1
        finally:
            print('---------------')

    print('Total proxies:', len(proxies))
    print('Good proxies:', g)
    print('Bad proxies:', b)

    with open('good_proxies.txt', 'w') as file:
        for item in good_proxies:
            file.write(item + '\n')


if __name__ == '__main__':
    url = 'https://www.myip.com/'
    main()
