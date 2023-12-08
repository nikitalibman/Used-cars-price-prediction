import all_dealers
import all_urls
import dataframe
import marks
import parsing
import sql_db


def main(pages, marks_menu):
    cars, characteristics, prices, locations = parsing.cars_info(pages)
    df = dataframe.df_construct(marks_menu, cars, characteristics, prices, locations)
    #sql_db.connect(df, 'append')
    return print(df)

if __name__ == '__main__':
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    marks_menu = marks.all_marks(url)
    dealers = all_dealers.main(url)
    pages = all_urls.main(dealers)
    main(pages, marks_menu)