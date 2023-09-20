#!/usr/bin/env python
# coding: utf-8

# In[113]:


import requests
from bs4 import BeautifulSoup
import csv


# In[114]:


url = 'https://www.autoscout24.com/lst/audi?atype=C&cy=A&desc=0&page=1&search_id=mmo9wqu7i8&sort=standard&source=listpage_pagination&ustate=N%2CU'
html = requests.get(url).text


# In[115]:


#get the number of total pages per every mark

soup = BeautifulSoup(html, 'lxml')
divs = soup.find('div', attrs={'class':'ListPage_pagination__v_4ci'})
pages = divs.find_all('button', attrs={'class':'FilteredListPagination_button__41hHM'})[-2].text
total_pages = int(pages)
print(total_pages)


# In[116]:


for i in range(1, total_pages + 1):
    url_parts = url.split('&')
    url_parts[3] = f'page={i}'
    url = '&'.join(url_parts)
    print(url)


# In[130]:


soup1 = BeautifulSoup(html, 'lxml')
models = soup1.find_all('div', attrs={'class':'ListItem_header__uPzec ListItem_header_new_design__hPPNh'})
n = 1
for model in models:
    model = model.find('h2')
    print(n, model.text)
    n+=1 

