"""
This module collects all URLs of the main pages from the website autoscout24.com.
"""

import requests
from bs4 import BeautifulSoup
from home_page import get_home_url
# from random_ua import main as user_agent


# get the number of total pages on the website
def total_pages(soup):
    try:
        indicator = soup.find('li', class_='pagination-item--disabled pagination-item--page-indicator')
        pages = int(indicator.text.split('/')[-1].strip())
        return pages
    except:
        print('Page indicator not found.')


# get a list of all URLs from every main page
def pages_urls(url, soup):
    all_pages = []
    try:
        for i in range(1, total_pages(soup) + 1):
            url_part = url.split('?')
            page_url = url_part[0] + f'?atype=C&desc=0&page={i}&search_id=m76u8v3lpc&sort=standard&source=listpage_pagination&ustate=N%2CU'
            all_pages.append(page_url)
        return all_pages
    except:
        print('No pages were found.')

def main(autoscout_url):
    # Here we provide URL to the very first main page.
    url = get_home_url(autoscout_url)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    return pages_urls(url, soup)


if __name__ == '__main__':
    autoscout_url = 'https://www.autoscout24.com/'
    print(main(autoscout_url))
