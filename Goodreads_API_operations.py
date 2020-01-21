#!/usr/bin/env python
# coding: utf-8

# In[63]:


import pandas as pd
import os
import goodreads_api_client as gr
import time

# selenium module
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException




# In[58]:


#goodreads_book_id: from selenium scraping


url_signin = 'https://www.goodreads.com/user/sign_in'
url = 'https://www.goodreads.com/shelf/show/public-domain'

goodreads_key = <key>
goodreads_secret = <secret>
def get_goodreadsbookid():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--lang=en");
    options.add_argument("--user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'")
    prefs = {"profile.default_content_setting_values.automatic_downloads": 1,
         "download.directory_upgrade": True,
         "safebrowsing.enabled": False,
         "safebrowsing.disable_download_protection": True,
         "intl.accept_languages": "en,en_US"}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome('C:/Users/priya/Downloads/chromedriver_win32/chromedriver', options=options) 
    driver.get(url_signin)
    username = driver.find_element_by_name('user[email]')
    username.send_keys()

    password = driver.find_element_by_name('user[password]')
    password.send_keys()
    form = driver.find_element_by_name('sign_in')
    form.submit()
    driver.get(url)
    list_href=[]
    list_title = []
    prev_url = url
    list_title=(driver.find_elements_by_class_name('bookTitle'))
    prev_url = driver.current_url
    for item in list_title:
        list_href.append(item.get_attribute('href'))
    next_elem = driver.find_element_by_class_name('next_page')
    next_elem.click()

    while driver.current_url!=prev_url:
        list_title=driver.find_elements_by_class_name('bookTitle')
        prev_url = driver.current_url
        for item in list_title:
            list_href.append(item.get_attribute('href'))
        next_elem = driver.find_element_by_class_name('next_page')
        next_elem.click()
       

    return list_href
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #driver.save_screenshot(os.environ['HOME'] + '/Development/Data Pipelines/1.png')  
    
    


# In[59]:


list_href = get_goodreadsbookid()


# In[61]:


bid = []
for li in list_href:
    s = li.split('show/')
    if s[1].find('-')==-1:
        bid.append(s[1].split('.')[0])
    else:
        bid.append(s[1].split('-')[0])


# In[73]:



#

client = gr.Client(developer_key=goodreads_key)
book_list = []

for i in bid:
    book = client.Book.show(i)
    time.sleep(1)
    print(i)
    try:
        i13 = book['isbn13']
    except:
        i13 = None
    try:
        title = book['title']
    except:    
        title = None
    try:
        kasin = book['kindle_asin']
    except:
        kasin = None
    try:
        yr = book['work']['original_publication_year']['#text']
    except:
        yr = '-'
    try:
        mnt = book['work']['original_publication_month']['#text']
    except:
        mnt = '-'
    book_tup = (i13,title,kasin,yr+'/'mnt)
    book_list.append(book_tup)
#df_pub_domain_titles_gr.append({'isbn13':book['isbn13'],'title':book['title'],'kindle_asin':book['kindle_asin'],'original_publication_date':book['work']['original_publication_year']['#text']+book['work']['original_publication_month']['#text']})
book_list


# In[76]:


df_pub_domain_titles_gr = pd.DataFrame(book_list,columns = ['isbn13' , 'title', 'kindle_asin' , 'original_publication_date']) 
df_pub_domain_titles_gr


# In[ ]:




