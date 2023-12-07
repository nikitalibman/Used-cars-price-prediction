"""
This module gathers links to all pages with cars from every dealer. The module works in concurrent threads. The output
is a full comprehensive list of all URLs with cars.
Execution time 1,5 minute (4.5 times faster than a sequential approach).
"""

from datetime import datetime
import concurrent.futures
import main_pages
import all_dealers


# This function extends dealers list of lists into 1 solid list.
# Then it deletes all href links that are longer than 60 characters.
# It returns a list of pages' URLs.

def preprocess(dealers):
    dealers_list = []
    for sublist in dealers:
        dealers_list.extend(sublist)
    filtered_list = [s for s in dealers_list if len(s) <= 60]
    return filtered_list


# This function returns a list of all dealers' pages using multithreading.
def multithread(pages):
    # Define a function to fetch data for a single page
    def fetch_page(href):
        return main_pages.pages_urls(href)
    # Use ProcessPoolExecutor to parallelize fetching data for multiple pages
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        all_dealer_pages = list(executor.map(fetch_page, pages))
    return all_dealer_pages


def main(dealers):
    pages = preprocess(dealers)
    all_dealer_pages = multithread(pages)
    extended_url_list = []
    for sublist in all_dealer_pages:
        extended_url_list.extend(sublist)
    return extended_url_list


if __name__ == '__main__':
    start = datetime.now()
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    dealers = all_dealers.main(url)
    main(dealers)
    end = datetime.now()
    print('Total time :', end - start)
