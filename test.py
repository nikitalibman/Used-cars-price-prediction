from datetime import datetime
import concurrent.futures
import main_pages
# import marks
# import parsing
# import dataframe
# import sql_db
import all_dealers


def main(pages):
    all_dealer_pages = []
    for href in pages:
        all_dealer_pages.append(main_pages.pages_urls(href))
    return all_dealer_pages

# cars, characteristics, prices, locations = parsing.cars_info(pages)  # first pages of every car dealer
# df = dataframe.df_construct(marks_menu, cars, characteristics, prices, locations)
# sql_db.connect(df, 'append')



if __name__ == '__main__':
    start = datetime.now()
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    pages = all_dealers.main(url)
    main(pages)
    end = datetime.now()
    print('Total time :', end - start)
