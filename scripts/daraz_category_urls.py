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
from decouple import config




from selenium import webdriver
driver = webdriver.Chrome(executable_path=config(CHROME_DRIVER_EXECUTABLE_PATH))
from selenium.webdriver.common.action_chains import ActionChains

import logging


user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    ]


def daraz_category_urls(baseurl, user_agent):

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

    driver.get(baseurl)
    
    time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    url_list = []
    # extract category urls from soup
    
    cat_elements = soup.find_all("li", {"class":"lzd-site-menu-root-item"})
    
    for cat_element in cat_elements:
        
        
        hover_element = driver.find_element_by_id(cat_element['id'])
        parent_cat_name = hover_element.text
        hover = ActionChains(driver).move_to_element(hover_element)
        hover.perform()
        # get html and find the url
        cat_element_soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        hover_soup = cat_element_soup.find_all("li", {"class":"lzd-site-menu-sub-item"})
        time.sleep(1)
        cat_url_list = []
        
        for hover_tag in hover_soup:
            # find all as
            #parent_cat_name = hover_tag.find("li", {"class": "lzd-site-menu-sub-item"})
            a_tags = hover_tag.find_all("a")
            for a in a_tags:
                url = "https:" + a['href']
                child_cat_name = a.text
                cat_url_list.append({'parent_category':parent_cat_name, 'child_category':child_cat_name, 'url':url})
            
        
    return cat_url_list


def get_url_list():

    baseurl = 'https://daraz.com.np/'

    url_list = daraz_category_urls(baseurl, user_agent_list[0])

    return url_list



# json_urls = json.dumps(url_list)

# text_file = open("daraz_cat_urls.txt", "w")
# text_file.write(json_urls)
# text_file.close()