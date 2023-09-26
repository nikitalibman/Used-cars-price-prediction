#!/usr/bin/env python
# coding: utf-8

# In[24]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


# In[25]:


url = 'https://www.autoscout24.com/lst?atype=C&desc=0&page=1&search_id=7ka6orz363&sort=standard&source=listpage_pagination&ustate=N%2CU'
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')


# In[26]:


#get the number of total pages on the web site
def total_pages(soup):
    divs = soup.find('div', attrs={'class':'ListPage_pagination__v_4ci'})
    pages = divs.find_all('button', attrs={'class':'FilteredListPagination_button__41hHM'})[-2].text
    total_pages = int(pages)
    return total_pages


# In[27]:


#get a dictionary of all URLs that lead to a specific page
all_pages = {}
for i in range(1, total_pages(soup) + 1):
    url_parts = url.split('&')
    url_parts[2] = f'page={i}'
    url = '&'.join(url_parts)
    all_pages[i]=url


# In[28]:


#here we create a list of html codes as soup elements about all pages
soups_list = []
for k in all_pages:
    soups_list.append(BeautifulSoup(requests.get(all_pages[k]).text, 'lxml'))


# In[49]:


cars = []
characteristics = []
prices = []
locations = []
for element in soups_list:
    car = element.find_all('a',attrs={'class':'ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l'})
    characters = element.find_all('div', attrs={'class':'VehicleDetailTable_container__mUUbY'})
    price = element.find_all('p', attrs={'class':'Price_price__WZayw PriceAndSeals_current_price__XscDn'})
    location = element.find_all('span', attrs={'class':'SellerInfo_address__txoNV'})
    for c, char, pr, loc in zip (car, characters, price, location):
        cars.append(c.get_text())
        characteristics.append(char.get_text())
        prices.append(pr.get_text())
        locations.append(loc.get_text())


# In[50]:


for i in range(len(cars)):
    cars[i] = cars[i].split('\xa0')[0]


# In[51]:


fuel_types = ['Gasoline','Diesel','Ethanol','Electric','Hydrogen','LPG','CNG','Electric/Gasoline','Others',
              'Electric/Diesel']
fuel_pattern = '|'.join(fuel_types)
gear = ['Automatic','Manual','Semi-automatic']
gear_pattern = '|'.join(gear)


# In[52]:


for i in range(len(characteristics)):
    patterns = [r'\d{1,3}(?:,\d{3})*\s?km', f'({gear_pattern})', r'\d{1,2}/\d{4}', f'({fuel_pattern})', r'\d{1,4}\s?hp']
    characteristics[i] = [re.search(pattern, characteristics[i]).group(0).replace(',', '').replace(' km', '').replace(' hp', '').strip() if re.search(pattern, characteristics[i]) else None for pattern in patterns]


# In[53]:


for i in range(len(prices)):
    prices[i] = int(re.sub(r'\D', '', prices[i]))


# In[54]:


for i in range(len(locations)):
    try:
        locations[i] = locations[i].split('• ')[1].split('-')[0]
    except:
        locations[i] = locations[i].split('-')[0]


# In[55]:


c = pd.Series(cars, name='Car')


# In[56]:


ch = pd.Series(characteristics)


# In[57]:


p = pd.Series(prices, name='Price [€]')


# In[58]:


l = pd.Series(locations, name='Location')


# In[59]:


# Create a DataFrame from the Series, which splits the lists into columns
df = pd.DataFrame(ch.tolist(), columns=['Mileage [km]', 'Transmission', 'Registration [m/y]', 'Fuel', 'Power [hp]'])


# In[60]:


df['Power [hp]'] = df['Power [hp]'].astype('int')
try:
    df['Mileage [km]'] = df['Mileage [km]'].astype('int')
except:
    df['Mileage [km]'] = df['Mileage [km]'].fillna(0)
    df['Mileage [km]'] = df['Mileage [km]'].astype('int')


# In[61]:


merged_df = pd.concat([c, df], axis=1)


# In[62]:


merged_df2 = pd.concat([merged_df,l], axis=1)


# In[63]:


merged_df3 = pd.concat([merged_df2,p], axis=1)


# In[64]:


merged_df3


# In[48]:


merged_df3.info()


# In[ ]:


https://www.autoscout24.com/lst?atype=C&cy=A&damaged_listing=exclude&desc=0&ocs_listing=include&powertype=kw&search_id=8dtdva8dsg&sort=standard&source=listpage_pagination&ustate=N%2CU


# In[ ]:


https://www.autoscout24.com/lst?atype=C&cy=B&damaged_listing=exclude&desc=0&ocs_listing=include&powertype=kw&search_id=xzvqpgg1qe&sort=standard&source=listpage_pagination&ustate=N%2CU

