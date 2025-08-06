import all_dealers
import all_urls
import dataframe
import marks
import parsing
import sql_db
import concurrent.futures
import threading

# Create a lock for the database connection
db_lock = threading.Lock()

def main(pages, marks_menu):
    def process_page(page):
        def parse_and_connect():
            nonlocal page
            cars, characteristics, prices, locations = parsing.cars_info(page)
            df = dataframe.df_construct(marks_menu, cars, characteristics, prices, locations)

            # Acquire the lock before connecting to the database
            with db_lock:
                sql_db.connect(df, 'append')

        # Use a separate thread for parsing and connecting to the database
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(parse_and_connect)

            # Wait for the task to complete
            concurrent.futures.wait([future])

    # Use ThreadPoolExecutor to parallelize processing for multiple pages
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Submit the tasks to the executor
        futures = [executor.submit(process_page, page) for page in pages]
        # Wait for all tasks to complete
        concurrent.futures.wait(futures)


if __name__ == '__main__':
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    marks_menu = marks.all_marks(url)
    dealers = all_dealers.main(url)
    pages = all_urls.main(dealers)
    main(pages, marks_menu)