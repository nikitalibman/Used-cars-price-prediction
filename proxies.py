import requests
from bs4 import BeautifulSoup
import re

def main(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml').text
    # Define a regular expression pattern to match IP addresses and ports
    pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+'
    proxy_servers = re.findall(pattern, soup)

    with open('proxies.txt', 'w') as f:
        for item in proxy_servers:
            f.write("%s\n" % item)

if __name__ == '__main__':
    url = 'https://free-proxy-list.net/'
    print(main(url))