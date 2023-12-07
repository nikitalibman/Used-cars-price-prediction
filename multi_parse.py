import all_dealers
import all_urls
import dataframe
import marks
import parsing
import sql_db
import concurrent.futures


def main(pages, marks_menu):
    # Function to perform the parsing and database connection
    def process_page(page):
        cars, characteristics, prices, locations = parsing.cars_info(page)
        df = dataframe.df_construct(marks_menu, cars, characteristics, prices, locations)
        sql_db.connect(df, 'append')

    # Use ThreadPoolExecutor to parallelize processing for multiple pages
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
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