import requests
url = 'https://httpbin.org/ip'
proxies = {
    "http": 'http://20.206.106.192:80',
    "https": 'http://20.206.106.192:80'
}
response = requests.get(url,proxies=proxies)
print(response.json())