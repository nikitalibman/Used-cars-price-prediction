"""
This module collects all URLs of the main pages from the website autoscout24.com.
"""

import requests
from bs4 import BeautifulSoup
from random_ua import main as user_agent


# Here we provide URL to the very first main page.

def pages_urls(url):
    html = requests.get(url, headers=user_agent()).text
    soup = BeautifulSoup(html, 'lxml')

    # get the number of total pages on the website
    def total_pages(soup):
        try:
            divs = soup.find('div', attrs={'class': 'ListPage_pagination__v_4ci'})
            pages = divs.find_all('button', attrs={'class': 'FilteredListPagination_button__41hHM'})[-2].text
            total_pages = int(pages)
            return total_pages
        except:
            pass

    # get a list of all URLs from every main page
    def pages_urls(url):
        all_pages = []
        try:
            for i in range(1, total_pages(soup) + 1):
                if len(url) > 100:
                    url_parts = url.split('&')
                    url_parts[2] = f'page={i}'
                else:
                    url = url + '&search_id=gxrsmwbnl8&source=listpage_pagination'
                    url_parts = url.split('&')
                    url_parts[2] = f'page={i}'
                url = '&'.join(url_parts)
                all_pages.append(url)
            return all_pages
        except:
            pass

    return pages_urls(url)


if __name__ == '__main__':
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    print(pages_urls(url))
