import requests
from bs4 import BeautifulSoup
import re
from random import choice, uniform
from time import sleep


def get_html(url, useragent, proxy):
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text


def get_ip(html):
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('div', attrs={'class': 'texto_1'}).text.strip()
    pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    ip = re.search(pattern, ip).group()
    user_agent = soup.find('div', attrs={'class': 'headers'}).find_next_sibling().text
    print(ip)
    print(user_agent)
    print('---------------')


def main():
    useragents = open('user_agents.txt').read().split('\n')
    proxies = open('proxies.txt').read().split('\n')

    for i in range(10):
        #sleep(uniform(3, 6))
        proxy = {'http': 'http://' + choice(proxies)}
        useragent = {'User-Agent': choice(useragents)}
        html = get_html(url, useragent, proxy)
        get_ip(html)


if __name__ == '__main__':
    url = 'https://www.myip.com/'
    main()
