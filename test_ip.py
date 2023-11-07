import requests
from random import choice

url_ip = 'https://httpbin.org/ip'
url_ua = 'https://httpbin.org//user-agent'
useragents = open('user_agents.txt').read().split('\n')[:-1]
proxies = open('good_proxies.txt').read().split('\n')[:-1]
random_proxy = choice(proxies)
proxies = {
    "http": 'http://' + random_proxy,
    "https": 'http://' + random_proxy
}

useragent = {'User-Agent': choice(useragents)}
response_ua = requests.get(url_ua, headers=useragent)
response_ip = requests.get(url_ip, proxies=proxies)
# requests.get(url_ip, headers=useragent, proxies=proxy)

print('UA :', response_ua.json())
print('IP :', response_ip.json())
