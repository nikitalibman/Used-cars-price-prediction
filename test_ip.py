import requests

url = 'https://httpbin.org/ip'
proxies = {
    "http": 'http://103.9.206.186:10008',
    "https": 'http://103.9.206.186:10008'
}
response = requests.get(url, proxies=proxies)
print(response.json())
