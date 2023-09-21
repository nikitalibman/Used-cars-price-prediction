#!/usr/bin/env python
# coding: utf-8

# In[6]:


import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver


# In[2]:


url = 'https://www.autoscout24.com/lst?atype=C&desc=0&page=1&search_id=7ka6orz363&sort=standard&source=listpage_pagination&ustate=N%2CU'
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')


# In[7]:


url1 = 'https://www.autoscout24.com/offers/mclaren-650s-coupe-lift-vollleder-parksystem-lm-stealth-finish-us-gasoline-black-e5d6e579-c0ca-4fec-8dcd-7f49e0625840?sort=standard&desc=0&lastSeenGuidPresent=true&cldtidx=2&position=2&search_id=mu46oz87ke&source_otp=t50&source=listpage_search-results&order_bucket=6'
html1 = requests.get(url1).text
soup1 = BeautifulSoup(html1, 'lxml')


# In[8]:


cars1 = soup1.find('a', attrs={'class':'scr-link StockList_link___HKPA'})
cars1


# In[ ]:


urls = []
for link in soup.find_all('a'):
    print(link.get('href'))


# In[ ]:


extract_href_with_selenium(url)


# In[ ]:


#get the number of total pages on the web site
def total_pages(soup):
    divs = soup.find('div', attrs={'class':'ListPage_pagination__v_4ci'})
    pages = divs.find_all('button', attrs={'class':'FilteredListPagination_button__41hHM'})[-2].text
    total_pages = int(pages)
    return total_pages


# In[ ]:


#get a dictionary of all URLs that lead to a specific page
all_pages = {}
for i in range(1, total_pages(soup) + 1):
    url_parts = url.split('&')
    url_parts[2] = f'page={i}'
    url = '&'.join(url_parts)
    all_pages[i]=url


# In[ ]:


page_1 = BeautifulSoup(requests.get(all_pages[1]).text, 'lxml')
more_cars = page_1.find('a', attrs={'class':'scr-link SellerInfo_link__Dmh0H'}).get('href')
more_cars


# In[ ]:


more_cars[0]


# In[ ]:


<a class="scr-link SellerInfo_link__Dmh0H" href="/lst?atype=C&amp;cid=15535338" rel="noopener">+ Show more vehicles</a>


# In[ ]:


href="/lst?atype=C&cid=15535338"


# In[ ]:


href="/lst?atype=C&cid=5791"


# In[ ]:


#here we get html codes as a soup element about all pages
soups_list = []
for k in all_pages:
    soups_list.append(BeautifulSoup(requests.get(all_pages[k]).text, 'lxml'))


# In[ ]:


#here we get description of mark and model about all cars from all the pages
for elem in soups_list:
    models = elem.find_all('div', attrs={'class':'ListItem_header__uPzec ListItem_header_new_design__hPPNh'})
    for model in models:
        model = model.find('h2')
        print(model.text)


# In[ ]:


#here we get info about all models and marks from one page
models = soup.find_all('div', attrs={'class':'ListItem_header__uPzec ListItem_header_new_design__hPPNh'})
n = 1
for model in models:
    model = model.find('h2')
    print(n, model.text)
    n+=1 


# In[ ]:


for elem in soups_list:
    elem.find_all('div', attrs={'class':'ListItem_header__uPzec ListItem_header_new_design__hPPNh'})
    


# In[ ]:


#here we get prices of all cars on one page
prices = soup.find_all('div', attrs={'class':'ListItem_listing__VjI4F'})
n = 1
for price in prices:
    price = price.find('p')
    print(n, price.text)
    n+=1 


# In[ ]:




