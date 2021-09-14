
import requests


product_url = 'https://www.daraz.com.np/#'



response = requests.get(product_url)

response.status_code

response.status_code



len(response.text)


page_contents = response.text


page_contents [:10000]


with open('webpage.html','w') as f:
    f.write(page_contents)


get_ipython().system('pip install beautifulsoup4 --upgrade --quiet')


from bs4 import BeautifulSoup



doc = BeautifulSoup(page_contents, 'html.parser')



type(doc)

