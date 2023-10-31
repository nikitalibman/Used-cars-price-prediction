import requests
import random_ip_agent

url = 'https://www.myip.com/'
proxy, useragent = random_ip_agent.rand()

try:
    response = requests.get("https://www.myip.com/", proxies=proxy)
    if response.status_code == 200:
        print("Proxy is working.")
        print(proxy)
    else:
        print("Proxy is not working.")
except Exception as e:
    print(f"Proxy error: {e}")
