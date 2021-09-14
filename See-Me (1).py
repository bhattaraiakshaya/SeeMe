#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install requests --upgrade --quiet')


# In[2]:


import requests


# In[3]:


product_url = 'https://www.daraz.com.np/#'


# In[4]:


response = requests.get(product_url)

response.status_code
# In[5]:


response.status_code


# In[6]:


len(response.text)


# In[7]:


page_contents = response.text


# In[8]:


page_contents [:10000]


# In[9]:


with open('webpage.html','w') as f:
    f.write(page_contents)


# In[10]:


#Use beautiful soup to parse and extract inforrmation#


# In[11]:


get_ipython().system('pip install beautifulsoup4 --upgrade --quiet')


# In[12]:


from bs4 import BeautifulSoup


# In[13]:


doc = BeautifulSoup(page_contents, 'html.parser')


# In[14]:


type(doc)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




