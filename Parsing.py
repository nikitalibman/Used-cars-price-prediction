#!/usr/bin/env python
# coding: utf-8

# # Scope of work
# 
# 1) Import all necessary libraries and modules.  
# 2) First we need to obtain inforamtion about all available cars from the first main pages.  
# 3) Create a SQL database and export there gathered info about cars from the main pages.  
# 4) Then we will call module dealers_cars to acquire links to every dealer's list of cars from all main pages.  
# 5) Now we will repeat the same procedure as in the 1st step but to the every dealer's cars list.  
# 6) Add extracted data to a created SQL database

# ## 1. Imort of libraries and modules

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from sqlalchemy import create_engine
import json
import dealers_cars
import marks


# ## 2. Acquring cars' information from the first main pages

# In[2]:


# Here we provide URL to the very first main page.


# In[3]:


url = 'https://www.autoscout24.com/lst?atype=C&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU'
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')


# In[4]:


#get the number of total pages on the web site
def total_pages(soup):
    divs = soup.find('div', attrs={'class':'ListPage_pagination__v_4ci'})
    pages = divs.find_all('button', attrs={'class':'FilteredListPagination_button__41hHM'})[-2].text
    total_pages = int(pages)
    return total_pages


# In[5]:


#get a dictionary of all URLs from every main page
def pages_urls(url):
    all_pages = {}
    for i in range(1, total_pages(soup) + 1):
        url_parts = url.split('&')
        url_parts[2] = f'page={i}'
        url = '&'.join(url_parts)
        all_pages[i]=url
    return all_pages

all_pages=pages_urls(url)


# In[6]:


#here we create a list of html codes as soup elements about all pages
def html_list():
    soups_list = []
    for k in all_pages:
        soups_list.append(BeautifulSoup(requests.get(all_pages[k]).text, 'lxml'))
    return soups_list

soups_list = html_list()


# In[7]:


# here we create blank lists to populate it later with cars' info
cars = []
characteristics = []
prices = []
locations = []

#this function scraps over the website in order to extract specific information about each car (characteristics, prices etc)
def parcing (tag, attr, df):
    for element in soups_list:
        info = element.find_all(tag, attrs={'class':attr})
        for i in info:
            df.append(i.get_text())
    return df


# In[8]:


#this function populate previously created blank lists with cars' info
def info():
    c = parcing('a', 'ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l', cars)
    ch = parcing('div', 'VehicleDetailTable_container__mUUbY', characteristics)
    p = parcing('p', 'Price_price__WZayw PriceAndSeals_current_price__XscDn', prices)
    l = parcing('span', 'SellerInfo_address__txoNV', locations)
    return c, ch, p, l


# In[9]:


cars, characteristics, prices, locations = info()


# r'\d{1,4}\s?hp'

# In[10]:


def formating():
    #here we extract only car's mark and maodel
    for i in range(len(cars)):
        cars[i] = cars[i].split('\xa0')[0]
    fuel_types = ['Gasoline','Diesel','Ethanol','Electric','Hydrogen','LPG','CNG','Electric/Gasoline','Others',
              'Electric/Diesel']
    fuel_pattern = '|'.join(fuel_types)
    gear = ['Automatic','Manual','Semi-automatic']
    gear_pattern = '|'.join(gear)
    #here we extract specific patterns of each car characteristics. The initial text that was extracted from web scraping
    #contains too much unrelated data
    for i in range(len(characteristics)):
        patterns = [r'\d{1,3}(?:,\d{3})*\s?km', f'({gear_pattern})', r'\d{1,2}/\d{4}', f'({fuel_pattern})', r'(\d{1,3}(?:,\d{3})*) hp']
        characteristics[i] = [re.search(pattern, characteristics[i]).group(0).replace(',', '').replace(' km', '')
                              .replace(' hp', '').strip() if re.search(pattern, characteristics[i])
                              else None for pattern in patterns]
    #here we extract integer from price text
    for i in range(len(prices)):
        prices[i] = int(re.sub(r'\D', '', prices[i]))
        
    #here we extract only country abbreveation
    for i in range(len(locations)):
        try:
            locations[i] = locations[i].split('• ')[1].split('-')[0]
        except:
            locations[i] = locations[i].split('-')[0]
            
    return cars, characteristics, prices, locations

cars, characteristics, prices, locations = formating()


# Here we call a module **marks** in order to extract all existing car marks from the website. Afterwards we will replace
# spaces in marks' names into dashes '-'

# In[11]:


marks_menu = marks.all_marks(url)


# In[12]:


space_names = []
for mark in marks_menu:
    if ' ' in mark:
        space_names.append(mark)


# In[13]:


# Here we create a dictionary where to each mark with a space in the name is assigned the same mark name but with a dash
mapping_dict = {}
for mark_with_space in space_names:
    mark_with_dash = mark_with_space.replace(" ", "-")
    mapping_dict[mark_with_space] = mark_with_dash

# This function performs replacement of cars' marks with spaces into dashes '-'
def replace_mark_name(name):
    for mark_with_space, mark_with_dash in mapping_dict.items():
        if mark_with_space in name:
            name = name.replace(mark_with_space, mark_with_dash)
    return name

# Apply replacements to list1
result = [replace_mark_name(item) for item in cars]

cars = result


# In[14]:


for car in range(len(cars)):
    cars[car] = cars[car].split(' ', 1)   


# In[16]:


# This function collects all previously formed lists and form 1 united dataframe in pandas
def to_pandas():
    #Here we transform our lists into pandas Series
    c = pd.DataFrame(cars, columns=['mark', 'model'])
    ch = pd.Series(characteristics)
    p = pd.Series(prices, name='price')
    l = pd.Series(locations, name='location')
    # Create a DataFrame from the Series, which splits the lists into columns
    df = pd.DataFrame(ch.tolist(), columns=['mileage', 'transmission', 'registration', 'fuel', 'power'])
    merged_df = pd.concat([c, df], axis=1)
    merged_df2 = pd.concat([merged_df,l], axis=1)
    main_pages_info = pd.concat([merged_df2,p], axis=1)
    return main_pages_info


# In[17]:


to_pandas()


# ## 3. Creating a SQL database and exporting parsed data there from the main pages

# In[18]:


# Load database configuration from a JSON file in order to avoid hardcoding sensible information
with open('postgres_configs.json') as config_file:
    config = json.load(config_file)


# In[19]:


#configurations to connect to a SQL database
db_user = config['postgres']['user']
db_password = config['postgres']['pwd']
db_host = config['postgres']['host']
db_port = config['postgres']['port']
db_name = config['postgres']['db']


# In[20]:


# Connection string
connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'


# In[21]:


engine = create_engine(connection_string)


# In[22]:


to_pandas().to_sql('cars', engine, if_exists='replace', schema='autoscout')


# ## 2. Acquiring links to every dealer's list of cars from all main pages.

# In[ ]:





# In[ ]:


# We call the module dealers_cars and assign the URL from the first main page
dealers_cars_list = dealers_cars.sel_pars(url)


# In[ ]:





# In[ ]:


dealers_cars_list


# In[ ]:


# Connection string
connection_string = 'postgresql://{}/{}@{}:{}/{}'.format(
    db_user,
    db_password,
    db_host,
    db_port,
    db_name
)


# In[ ]:


s = set(dealers_cars_list)


# In[ ]:


s


# In[ ]:


#with engine.connect() as conn:
#    conn.execute('CREATE SCHEMA IF NOT EXISTS cars_small;')


# In[ ]:


#with engine.connect() as conn:
#    to_pandas().to_sql(name='cars_info', con=conn, if_exists='replace', index=False)


# In[ ]:


dealers_cars_list[0]


# In[ ]:


url0 = dealers_cars_list[0]
html0 = requests.get(url0).text
soup0 = BeautifulSoup(html0, 'lxml')


# In[ ]:


total_pages(soup0)


# In[ ]:




