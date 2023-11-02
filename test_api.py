import requests
import random_ip_agent


url = 'https://api.myip.com/'
#proxy, useragent = random_ip_agent.rand()

proxy = {'http': 'http://43.157.8.79:8888',
         "https": 'https://43.157.8.79:8888'}

response = requests.get(url, proxies=proxy).text
print(response)
