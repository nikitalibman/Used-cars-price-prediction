#!/usr/bin/env python
# coding: utf-8

# This Parsing module serves to scrap all data about cars from the first main pages of the website autoscout24.com.
# The output of this module are several lists with cars' information: cars names, characteristics, locations, prices.

import requests
from bs4 import BeautifulSoup
import re


# Here we provide URL to the very first main page.

def cars_info(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')

    # get the number of total pages on the web site
    def total_pages(soup):
        divs = soup.find('div', attrs={'class': 'ListPage_pagination__v_4ci'})
        pages = divs.find_all('button', attrs={'class': 'FilteredListPagination_button__41hHM'})[-2].text
        total_pages = int(pages)
        return total_pages

    # get a dictionary of all URLs from every main page
    def pages_urls(url):
        all_pages = {}
        for i in range(1, total_pages(soup) + 1):
            if len(url) > 100:
                url_parts = url.split('&')
                url_parts[2] = f'page={i}'
            else:
                url = url+'&search_id=gxrsmwbnl8&source=listpage_pagination'
                url_parts = url.split('&')
                url_parts[2] = f'page={i}'
            url = '&'.join(url_parts)
            all_pages[i] = url
        return all_pages

    all_pages = pages_urls(url)

    # here we create a list of html codes as soup elements about all pages
    def html_list():
        soups_list = []
        for k in all_pages:
            soups_list.append(BeautifulSoup(requests.get(all_pages[k]).text, 'lxml'))
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
            info = element.find_all(tag, attrs={'class': attr})
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


if __name__ == "__main__":
    #url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    url = 'https://www.autoscout24.com/lst?atype=C&cid=27583740'
    print(cars_info(url))
