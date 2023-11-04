import requests
from random import choice


url = 'https://api.myip.com/'

proxies = open('proxyscrape_premium_http_proxies.txt').read().split('\n')[:-1]

for i in range(10):
    random_proxy = choice(proxies)
    proxy = {'http': 'http://' + random_proxy,
             "https": 'http://' + random_proxy}
    response = requests.get(url, proxies=proxy).text
    print(response)
