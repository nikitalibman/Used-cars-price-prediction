import requests
import socket
import random_ip_agent

url = 'autoscout24.com'

proxy, useragent = random_ip_agent.rand()

hostname = socket.gethostbyname(url)

headers = {'Host': url}

# Create a session and specify the 'server_hostname' parameter for the HTTPS connection
with requests.Session() as session:
    session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))

    response = session.get('https://'+url, proxies=proxy, headers=headers)

# Make the request
#response = requests.get(url).text
print(response)
print(proxy)
print(useragent)


