"""
This module extracts html codes from a list of pages that is provided as an argument in the main cars_info
function. Then it scraps info about every car from every page.
The output of this module are several lists with cars' information: cars names, characteristics, locations, prices.
"""


import requests
from bs4 import BeautifulSoup
import re
import main_pages


def cars_info(all_pages):
    # here we create a list of html codes as soup elements about all pages
    def html_list():
        soups_list = []
        if all_pages is not None:
            for k in all_pages:
                try:
                    soups_list.append(BeautifulSoup(requests.get(k).text, 'lxml'))
                except:
                    continue
        return soups_list

    soups_list = html_list()

    # here we create blank lists to populate it later with cars' info
    cars = []
    characteristics = []
    prices = []
    locations = []

    # this function scraps over the website in order to extract specific information about each car (characteristics,
    # prices etc)
    def parcing(tag, attr, df):
        for element in soups_list:
            try:
                info = element.find_all(tag, attrs={'class': attr})
            except:
                continue
            for i in info:
                df.append(i.get_text())
        return df

    # this function populate previously created blank lists with cars' info
    def info():
        c = parcing('a', 'ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l', cars)
        ch = parcing('div', 'VehicleDetailTable_container__mUUbY', characteristics)
        p = parcing('p', 'Price_price__WZayw PriceAndSeals_current_price__XscDn', prices)
        l = parcing('span', 'SellerInfo_address__txoNV', locations)
        return c, ch, p, l

    cars, characteristics, prices, locations = info()

    def formating():
        # here we extract only car's mark and maodel
        for i in range(len(cars)):
            cars[i] = cars[i].split('\xa0')[0]
        fuel_types = ['Gasoline', 'Diesel', 'Ethanol', 'Electric', 'Hydrogen', 'LPG', 'CNG', 'Electric/Gasoline',
                      'Others', 'Electric/Diesel']
        fuel_pattern = '|'.join(fuel_types)
        gear = ['Automatic', 'Manual', 'Semi-automatic']
        gear_pattern = '|'.join(gear)
        # here we extract specific patterns of each car characteristics. The initial text that was extracted from web
        # scraping contains too much unrelated data
        for i in range(len(characteristics)):
            patterns = [r'\d{1,3}(?:,\d{3})*\s?km', f'({gear_pattern})', r'\d{1,2}/\d{4}', f'({fuel_pattern})',
                        r'(\d{1,3}(?:,\d{3})*) hp']
            characteristics[i] = [re.search(pattern, characteristics[i]).group(0).replace(',', '').replace(' km', '')
                                      .replace(' hp', '').strip() if re.search(pattern, characteristics[i])
                                  else None for pattern in patterns]
        # here we extract integer from price text
        for i in range(len(prices)):
            prices[i] = int(re.sub(r'\D', '', prices[i]))

        # here we extract only country abbreviation
        for i in range(len(locations)):
            try:
                locations[i] = locations[i].split('• ')[1].split('-')[0]
            except:
                locations[i] = locations[i].split('-')[0]

        return cars, characteristics, prices, locations

    cars, characteristics, prices, locations = formating()

    return cars, characteristics, prices, locations


if __name__ == '__main__':
    url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    all_pages = main_pages.pages_urls(url)
    print(cars_info(all_pages))
