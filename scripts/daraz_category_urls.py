#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 08:38:33 2021

@author: akshayabhattarai
"""

import time
from bs4 import BeautifulSoup
import pandas as pd
import json
import logging
# from decouple import config
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from agent_rotation import *

from constants import *

# test, helper function
def get_list_cat_elements(cat_elements):
    list_cat_elements = []
    for cat_element in cat_elements:
        list_cat_elements.append(cat_element)
    return list_cat_elements



def daraz_category_urls(proxies, baseurl):

    driver = get_driver(proxies)

    # driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    # exception handling (timeout)
    driver.get(baseurl)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    time.sleep(5)
    
    timeout = DARAZ_DRIVER_TIMEOUT
    try:
        element_present = EC.presence_of_element_located((By.ID, 'element_id'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    # extract category urls from soup
    cat_elements = soup.find_all(DARAZ_CATEGORY_ROOT_MENU_TAG, {"class": DARAZ_CATEGORY_ROOT_MENU_CLASSNAME})
    
    category_tree = []
    
    for cat_element in cat_elements:
        
        l1_category_elements = driver.find_element_by_id(cat_element['id'])
        l1_category = l1_category_elements.text
        
        l2_classname = DARAZ_CATEGORY_SUB_MENU_CLASSNAME + " " + cat_element['id']
        l2_category_element = soup.find('ul', {'class':l2_classname})
        l2_category_elements = l2_category_element.find_all(DARAZ_CATEGORY_SUB_MENU_ITEM_TAG, {'class':DARAZ_CATEGORY_SUB_MENU_ITEM} )
        

        for l2_category_element in l2_category_elements:

            l2_category = l2_category_element.span.text
            l2_url = "https:" + l2_category_element.a['href']

            l3_category_elements = l2_category_element.find(DARAZ_CATEGORY_L2_TABLE_TAG, {'class': DARAZ_CATEGORY_L2_TABLE})
            l3_category_elements = l3_category_elements.find_all(DARAZ_CATEGORY_L2_ITEM_TAG, {'class': DARAZ_CATEGORY_L2_ITEM})
            
            for l3_category_element in l3_category_elements:
                l3_category = l3_category_element.span.text
                a_tag = l3_category_element.find('a')
                l3_url = "https:" + a_tag['href']

                category_tree.append({'l1_Cat': l1_category, 'l2_cat': l2_category, 'l3_cat':l3_category, 'l2_url':l2_url, 'l3_url': l3_url})

    driver.close()
    return category_tree
            



def get_url_list(proxies):
    baseurl = 'https://daraz.com.np/'
    url_list = daraz_category_urls(proxies, baseurl)
    return url_list


if __name__ == '__main__':
    proxies = get_proxies()
    # proxies = []
    baseurl = 'https://daraz.com.np/'
    url_list = daraz_category_urls(proxies, baseurl)
    cat_tree_df = pd.DataFrame(url_list)
    cat_tree_df.to_csv('daraz_category_tree.csv')
