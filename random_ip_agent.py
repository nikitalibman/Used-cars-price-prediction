"""
This module randomly selects one Proxy Server and one User Agent from the previously formed txt files:
proxies.txt and user_agents.txt. This pair will be used afterward in the module dealers_cars.py in order to
perform multiple simultaneous requests to the website and avoid a ban.
"""

from random import choice


def rand():
    useragents = open('user_agents.txt').read().split('\n')[:-1]
    proxies = open('http_proxies.txt').read().split('\n')[:-1]
    random_proxy = choice(proxies)
    proxy = {
       'http': 'http://' + random_proxy,
        'https': 'https://' + random_proxy
    }
    #proxy = {'http': 'http://' + choice(proxies),
    #         "https": 'https://' + choice(proxies)}
    useragent = {'User-Agent': choice(useragents)}
    return proxy, useragent


if __name__ == '__main__':
    print(rand())
