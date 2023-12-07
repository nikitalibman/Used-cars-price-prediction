"""
This module gathers links to car dealers from all the main 20 pages. The script works in parallel processes. The output
is a list of all dealers' URLs (first main page of every dealer). Execution time 19 minutes.
"""

import multiprocessing
from datetime import datetime
import main_pages
import dealers_buttons_multithread

def process_page(page):
    return dealers_buttons_multithread.main(page)

def main(url):
    all_pages = main_pages.pages_urls(url)

    # Create a pool of processes
    pool = multiprocessing.Pool(processes=4)

    # Map the process_page function to each page in all_pages
    dealers_urls = pool.map(process_page, all_pages)

    # Close the pool and wait for the worker processes to finish
    pool.close()
    pool.join()

    return dealers_urls

if __name__ == '__main__':
    start = datetime.now()
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    dealers = main(url)
    #print(dealers)
    end = datetime.now()
    print('Total time :', end - start)
