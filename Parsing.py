#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from sqlalchemy import create_engine
import sel_part

# In[2]:


url = 'https://www.autoscout24.com/lst?atype=C&desc=0&page=1&search_id=7ka6orz363&sort=standard&source=listpage_pagination&ustate=N%2CU'
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')


# In[3]:


# get the number of total pages on the web site
def total_pages(soup):
    divs = soup.find('div', attrs={'class': 'ListPage_pagination__v_4ci'})
    pages = divs.find_all('button', attrs={'class': 'FilteredListPagination_button__41hHM'})[-2].text
    total_pages = int(pages)
    return total_pages


# In[4]:


# get a dictionary of all URLs that lead to a specific page
all_pages = {}
for i in range(1, total_pages(soup) + 1):
    url_parts = url.split('&')
    url_parts[2] = f'page={i}'
    url = '&'.join(url_parts)
    all_pages[i] = url

# In[5]:


# here we create a list of html codes as soup elements about all pages
soups_list = []
for k in all_pages:
    soups_list.append(BeautifulSoup(requests.get(all_pages[k]).text, 'lxml'))

# In[31]:


# here we create blank lists to populate it later with cars' info
cars = []
characteristics = []
prices = []
locations = []


# this function scraps over the website in order to extract specific information about each car (characteristics, prices etc)
def parcing(tag, attr, df):
    for element in soups_list:
        info = element.find_all(tag, attrs={'class': attr})
        for i in info:
            df.append(i.get_text())
    return df


# In[32]:


# here we call the above mentioned function and populate our previously created lists
cars = parcing('a', 'ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l', cars)
characteristics = parcing('div', 'VehicleDetailTable_container__mUUbY', characteristics)
prices = parcing('p', 'Price_price__WZayw PriceAndSeals_current_price__XscDn', prices)
locations = parcing('span', 'SellerInfo_address__txoNV', locations)

# In[33]:


# here we extract only car's mark and maodel
for i in range(len(cars)):
    cars[i] = cars[i].split('\xa0')[0]

# In[34]:


fuel_types = ['Gasoline', 'Diesel', 'Ethanol', 'Electric', 'Hydrogen', 'LPG', 'CNG', 'Electric/Gasoline', 'Others',
              'Electric/Diesel']
fuel_pattern = '|'.join(fuel_types)
gear = ['Automatic', 'Manual', 'Semi-automatic']
gear_pattern = '|'.join(gear)

# In[35]:


# here we extract specific patterns of each car characteristics. The initial text that was extracted from web scraping
# contains too much unrelated data
for i in range(len(characteristics)):
    patterns = [r'\d{1,3}(?:,\d{3})*\s?km', f'({gear_pattern})', r'\d{1,2}/\d{4}', f'({fuel_pattern})', r'\d{1,4}\s?hp']
    characteristics[i] = [
        re.search(pattern, characteristics[i]).group(0).replace(',', '').replace(' km', '').replace(' hp',
              '').strip() if re.search(
            pattern, characteristics[i]) else None for pattern in patterns]

# In[36]:


# here we extract integer from price text
for i in range(len(prices)):
    prices[i] = int(re.sub(r'\D', '', prices[i]))

# In[37]:


# here we extract only country abbreveation
for i in range(len(locations)):
    try:
        locations[i] = locations[i].split('• ')[1].split('-')[0]
    except:
        locations[i] = locations[i].split('-')[0]

# In[13]:


c = pd.Series(cars, name='Car')

# In[14]:


ch = pd.Series(characteristics)

# In[15]:


p = pd.Series(prices, name='Price [€]')

# In[16]:


l = pd.Series(locations, name='Location')

# In[17]:


# Create a DataFrame from the Series, which splits the lists into columns
df = pd.DataFrame(ch.tolist(), columns=['Mileage [km]', 'Transmission', 'Registration [m/y]', 'Fuel', 'Power [hp]'])

# In[18]:


try:
    df['Mileage [km]'] = df['Mileage [km]'].astype('int')
    df['Power [hp]'] = df['Power [hp]'].astype('int')
except:
    df['Power [hp]'] = df['Power [hp]'].fillna(0)
    df['Power [hp]'] = df['Power [hp]'].astype('int')
    df['Mileage [km]'] = df['Mileage [km]'].fillna(0)
    df['Mileage [km]'] = df['Mileage [km]'].astype('int')

# In[19]:


merged_df = pd.concat([c, df], axis=1)

# In[20]:


merged_df2 = pd.concat([merged_df, l], axis=1)

# In[21]:


merged_df3 = pd.concat([merged_df2, p], axis=1)

# In[22]:


merged_df3

# In[23]:


merged_df3.info()

# In[24]:


# configurations to connect to a SQL database
db_config = {
    'user': 'postgres',
    'pwd': 'austria011020',
    'host': 'localhost',
    'port': 5432,
    'db': 'cars_small'
}

# In[25]:


connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(
    db_config['user'],
    db_config['pwd'],
    db_config['host'],
    db_config['port'],
    db_config['db'],
)

# In[26]:


engine = create_engine(connection_string)

# In[29]:


with engine.connect() as conn:
    conn.execute('CREATE SCHEMA IF NOT EXISTS cars_small;')

# In[30]:


with engine.connect() as conn:
    merged_df3.to_sql(name='cars_info', schema='cars_small', con=conn, if_exists='replace', index=False)

