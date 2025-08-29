from urllib.parse import urlparse, parse_qs

car1 = '34911bad-64d8-4715-bcec-fed4969e3af3'
car2 = '4edfc01e-d576-4834-a095-150cf2bb4eeb'
car3 = '20e3148f-ffe5-4130-836c-b1cae4913ed9'


dealers = {'https://www.autoscout24.com/lst?_gl=1%2Ahufuc7%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=34113&page=1&search_id=hu42k4nyes&source=listpage_pagination': 6, 
           'https://www.autoscout24.com/lst?_gl=1%2Ahufuc7%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=48744261&page=1&search_id=tibgpdi1m6&source=listpage_pagination': 1, 
           'https://www.autoscout24.com/lst?_gl=1%2Ahufuc7%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=50746317&page=1&search_id=k62aui3aat&source=listpage_pagination': 1, 
           'https://www.autoscout24.com/lst?_gl=1%2Ahufuc7%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=47539916&page=1&search_id=gqhf0ofrfm&source=listpage_pagination': 1, 
           'https://www.autoscout24.com/lst?_gl=1%2A1nmy0op%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=21326&page=1&search_id=14tanw3pxgq&source=listpage_pagination': 2, 
           'https://www.autoscout24.com/lst?_gl=1%2A1nmy0op%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=6799766&page=1&search_id=ru9qyzl16w&source=listpage_pagination': 7, 
           'https://www.autoscout24.com/lst?_gl=1%2A1nmy0op%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=28165&page=1&search_id=10cgxjt2dae&source=listpage_pagination': 1, 
           'https://www.autoscout24.com/lst?_gl=1%2A1nmy0op%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=3768864&page=1&search_id=y1lwoal9ym&source=listpage_pagination': 7, 
           'https://www.autoscout24.com/lst?_gl=1%2A1nmy0op%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=16108825&page=1&search_id=17qapas1rhb&source=listpage_pagination': 11,
           'https://www.autoscout24.com/lst?_gl=1%2Aklobxt%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=4192049&page=1&search_id=9ruxwis8un&source=listpage_pagination': 9, 
           'https://www.autoscout24.com/lst?_gl=1%2Aklobxt%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=36185183&page=1&search_id=d4w7vtbpi7&source=listpage_pagination': 2, 
           'https://www.autoscout24.com/lst?_gl=1%2Aklobxt%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=5709&page=1&search_id=51tt1nio0n&source=listpage_pagination': 20, 
           'https://www.autoscout24.com/lst?_gl=1%2Aklobxt%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=12362805&page=1&search_id=bphta42jsl&source=listpage_pagination': 2, 
           'https://www.autoscout24.com/lst?_gl=1%2Aklobxt%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=6676070&page=1&search_id=roxzq7e9oq&source=listpage_pagination': 5, 
           'https://www.autoscout24.com/lst?_gl=1%2A1pbg7a7%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=42350494&page=1&search_id=smh5fhaye&source=listpage_pagination': 1, 
           'https://www.autoscout24.com/lst?_gl=1%2A1pbg7a7%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=11076&page=1&search_id=14xsifyabv2&source=listpage_pagination': 5, 
           'https://www.autoscout24.com/lst?_gl=1%2A1pbg7a7%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=10341&page=1&search_id=uptyy9lhag&source=listpage_pagination': 6, 
           'https://www.autoscout24.com/lst?_gl=1%2A1pbg7a7%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=49062556&page=1&search_id=xbzbo6w7io&source=listpage_pagination': 2, 
           'https://www.autoscout24.com/lst?_gl=1%2A1pbg7a7%2A_up%2AMQ..%2A_ga%2AMjEyODQ3MDYzOS4xNzU2NDc1OTAz%2A_ga_BGSHTTTQ7W%2AczE3NTY0NzU5MDIkbzEkZzAkdDE3NTY0NzU5MDIkajYwJGwwJGgw&atype=C&cid=20203195&page=1&search_id=b2x1os5oz5&source=listpage_pagination': 4}

for dealer in dealers.items():
    all_urls = []
    #page_number = list(dealers.keys())[0].split('page=')[1].split('&')[0]
    url_before_page_number = list(dealers.keys())[0].split('page=')[0]
    after = list(dealers.keys())[0].split('page=')[1].split('&')[1]
    for page in range(1, list(dealer)[1]):
        whole = f'{url_before_page_number}page={page}&{after}'
        all_urls.append(whole)
print(all_urls)



# for dealer in dealers.items():
#     print(list(dealer)[1])

