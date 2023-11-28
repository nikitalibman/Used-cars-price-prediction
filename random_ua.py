"""
This module randomly selects one User Agent from the previously formed txt file user_agents.txt. This user agent
will be used afterward in the module multiprocess_test.py in order to perform multiple simultaneous requests to the
website and avoid a ban.
"""

from random import choice


def main():
    with open('user_agents.txt') as ua_file:
        useragents = ua_file.read().split('\n')[:-1]
    useragent = {'User-Agent': choice(useragents)}
    return useragent


if __name__ == '__main__':
    print(main())
