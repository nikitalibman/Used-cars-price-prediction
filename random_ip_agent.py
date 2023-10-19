from random import choice


def rand():
    useragents = open('user_agents.txt').read().split('\n')[:-1]
    proxies = open('proxies.txt').read().split('\n')[:-1]
    proxy = {'http': 'http://' + choice(proxies),
             "https": 'http://' + choice(proxies)}
    useragent = {'User-Agent': choice(useragents)}
    return proxy, useragent


if __name__ == '__main__':
    print(rand())
