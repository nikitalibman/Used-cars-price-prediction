#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re


# In[2]:


url = 'https://www.autoscout24.com/lst?atype=C&desc=0&page=1&search_id=7ka6orz363&sort=standard&source=listpage_pagination&ustate=N%2CU'
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')


# In[3]:


#get the number of total pages on the web site
def total_pages(soup):
    divs = soup.find('div', attrs={'class':'ListPage_pagination__v_4ci'})
    pages = divs.find_all('button', attrs={'class':'FilteredListPagination_button__41hHM'})[-2].text
    total_pages = int(pages)
    return total_pages


# In[4]:


#get a dictionary of all URLs that lead to a specific page
all_pages = {}
for i in range(1, total_pages(soup) + 1):
    url_parts = url.split('&')
    url_parts[2] = f'page={i}'
    url = '&'.join(url_parts)
    all_pages[i]=url


# In[5]:


#here we create a list of html codes as soup elements about all pages
soups_list = []
for k in all_pages:
    soups_list.append(BeautifulSoup(requests.get(all_pages[k]).text, 'lxml'))


# In[6]:


cars = []
characteristics = []
prices = []
for element in soups_list:
    car = element.find_all('a',attrs={'class':'ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l'})
    characters = element.find_all('div', attrs={'class':'VehicleDetailTable_container__mUUbY'})
    price = element.find_all('p', attrs={'class':'Price_price__WZayw PriceAndSeals_current_price__XscDn'})
    for c, char, pr in zip (car, characters, price):
        cars.append(c.get_text())
        characteristics.append(char.get_text())
        prices.append(pr.get_text())


# In[18]:


for i in range(len(cars)):
    cars[i] = cars[i].split('\xa0')[0]


# In[33]:


for i in range(len(characteristics)):
    patterns = [r'\d{1,3}(?:,\d{3})*\s?km', r'Automatic|Manual', r'\d{1,2}/\d{4}', r'Diesel|Gasoline|Petrol|Electric', r'\d{1,4}\s?hp']
    characteristics[i] = [re.search(pattern, characteristics[i]).group(0).replace(' km', '').strip() if re.search(pattern, characteristics[i]) else None for pattern in patterns]


# In[39]:


for i in range(len(prices)):
    prices[i] = int(re.sub(r'\D', '', prices[i]))


# In[ ]:




