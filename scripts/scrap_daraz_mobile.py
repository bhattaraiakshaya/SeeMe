#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 20:46:55 2021

@author: akshayabhattarai

NOTE: #######################

download chrome driver exe from https://chromedriver.chromium.org/downloads
set env var - 'CHROME_DRIVER_EXECUTABLE_PATH' to chrome driver exe
edit demo.env file and save it as .env

#################################

"""


import time
from bs4 import BeautifulSoup
import pandas as pd
import logging
from decouple import config

from selenium import webdriver
driver = webdriver.Chrome(executable_path=config('CHROME_DRIVER_EXECUTABLE_PATH'))



# constants

## class names
product_card_tag_type = "div"
product_card_class_name = "c3KeDq"

product_name_tag_type = "div"
product_name_class_name = "c16H9d"


product_price_tag_type = "span"
product_price_class_name = "c13VH6"

og_price_tag_type = "del"
og_price_class_name = "c13VH6"

discount_percent_tag_type = "span"
discount_percent_class_name = "c1hkC1"

review_count_tag_type = "span"
review_count_class_name = "c3XbGJ"



user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    ]



# using seleneum driver
def get_soup_from_url(url, user_agent):
    
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

    driver.get(url)
    
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # html_str = driver.page_source
    
    # with open('html_py.html', 'w') as f:
    #     f.write(html_str)
    # f.close()
    
    #driver.quit()
    return soup



# get product object from tag
def extract_product_from_tag(tag):
    product_dict = dict()
    
    
    name = tag.find(product_name_tag_type, {"class":product_name_class_name})
    if name:
        product_dict['name'] = name.text
    else:
        product_dict['name'] = None
    
    
    price = tag.find(product_price_tag_type, {"class": product_price_class_name})
    if price:
        product_dict['price'] = price.text
    else:
        product_dict['price'] = None
        
        
    og_price = tag.find(og_price_tag_type, {"class":og_price_class_name})
    if og_price:
        product_dict['og_price'] = og_price.text
    else:
        product_dict['og_price'] = None
        
    discount_percent = tag.find(discount_percent_tag_type, {"class":discount_percent_class_name})
    if discount_percent:
        product_dict['discount_percent'] = discount_percent.text
    else:
        product_dict['discount_percent'] = None

    review_count = tag.find(review_count_tag_type, {"class":review_count_class_name})
    if review_count:
        product_dict['review_count'] = review_count.text
    else:
        product_dict['review_count'] = None
    
    
    return product_dict


# find and isolate all product card elements
# product_card
def process_soup(soup):
    # find all divs with classname - c3KeDq
    # list of all product card divs
    product_card_divs = soup.find_all("div", {"class": product_card_class_name})
    
    product_list = []
    for tag in product_card_divs:
        product = extract_product_from_tag(tag)
        product_list.append(product)
    return product_list
    


product_list = []
total_pages = 3
for i in range(total_pages -1):
    print('i -- ' , i+1)
    page = i + 1
    url = f'https://www.daraz.com.np/smartphones/?page={page}&spm=a2a0e.searchlistcategory.breadcrumb.3.2bcb7f45x4iDpp'
    #url = f'https://www.daraz.com.np/phones-tablets/?page={page}&spm=a2a0e.searchlistcategory.breadcrumb.2.63353056mFjhIN'
    
    # user_agent rotation
    user_agent = user_agent_list[ (i%len(user_agent_list)) ]
    
    logging.info('url - \n {url} \n user_agent index - {(i%len(user_agent_list))}')
    
    soup = get_soup_from_url(url, user_agent)
    cur_product_list = process_soup(soup)
    
    product_list = product_list + cur_product_list
    
    logging.info(f'cur product list = {len(cur_product_list)} \n cumulative product list  = {len(product_list)}')

logging.info(f'all pages complete \n total products = {len(product_list)}')
driver.quit()
product_df = pd.DataFrame(product_list)

#product_df.to_csv('daraz_mobile_and_tablets.csv')


