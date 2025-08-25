"""
This module extracts html codes from a list of pages that is provided as an argument in the main cars_info
function. Then it scraps info about every car from every page.
The output of this module are several lists with cars' information: cars names, characteristics, locations, prices.
"""


import requests
from bs4 import BeautifulSoup
import re
import main_pages as mp


def get_main_htmls(all_pages):
    """Create a list of html codes as soup elements about all main pages."""
    soups_list = []
    if all_pages is not None:
        for k in all_pages:
            try:
                soups_list.append(BeautifulSoup(requests.get(k).text, 'lxml'))
            except:
                continue
    return soups_list


def parce_car_info(soups_list, tag, attr, df):
    """This function scraps over the website in order to extract specific information about each car (characteristics, prices etc)"""
    for element in soups_list:
        try:
            info = element.find_all(tag, attrs={'class': attr})
        except:
            continue
        for i in info:
            df.append(i.get_text())
    return df


def create_car_dataframes(soups_list):
    """Create blank lists and populate them with cars' info"""
    cars = []
    characteristics = []
    prices = []
    locations = []
    cars = parce_car_info(soups_list, 'span',
                          'ListItem_title_bold__iQJRq', cars)
    characteristics = parce_car_info(
        soups_list, 'div', 'VehicleDetailTable_container__XhfV1', characteristics)
    prices = parce_car_info(
        soups_list, 'prices', 'Price_price__APlgs PriceAndSeals_current_price__ykUpx', prices)
    locations = parce_car_info(
        soups_list, 'span', 'SellerInfo_address__leRMu', locations)
    return cars, characteristics, prices, locations


def format_cars_info(characteristics, prices, locations):
    """Format cars' info about characteristics, prices, locations"""

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

    return characteristics, prices, locations


def main(url):
    all_pages = mp.main(url)
    soups_list = get_main_htmls(all_pages)
    cars, characteristics, prices, locations = create_car_dataframes(
        soups_list)
    format_cars_info(characteristics, prices, locations)
    return cars, characteristics, prices, locations


if __name__ == '__main__':
    url = 'https://www.autoscout24.com/'
    print(main(url))
