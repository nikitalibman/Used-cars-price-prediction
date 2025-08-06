"""
This module collects all URLs of the main pages from the website autoscout24.com.
"""

import requests
from bs4 import BeautifulSoup
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
        print(all_pages)
    except:
        print('No pages were found.')

def main(url):
    # Here we provide URL to the very first main page.
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    pages_urls(url, soup)


if __name__ == '__main__':
    url = 'https://www.autoscout24.com/lst?sort=standard&desc=0&ustate=N%2CU&atype=C&cy=D%2CA%2CI%2CB%2CNL%2CE%2CL%2CF&cat=&source=homepage_search-mask'
    main(url)
