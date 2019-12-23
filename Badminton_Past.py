#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup 
import datetime
from selenium import webdriver
import pandas as pd


# # 3F羽球場

# In[161]:


columns = []


# In[171]:


# 522 weeks = 10 years, starts from 2009/12/18
for l in range(523):
    y = (datetime.datetime(2009, 12, 18) + datetime.timedelta(days= l * 7)).year
    m = (datetime.datetime(2009, 12, 18) + datetime.timedelta(days= l * 7)).month
    d = (datetime.datetime(2009, 12, 18) + datetime.timedelta(days= l * 7)).day
    query_date = str(y) + "/" + str(m) + "/" + str(d)

    url = 'https://ntupesc.ntu.edu.tw/facilities/PlaceGrd.aspx?nFlag=0&placeSeq=1&dateLst='
    url += query_date
    r = requests.get(url)

    if r.status_code == requests.codes.ok: # OK!
        print("OK!" + str(l+1))
        
    column = []
    for k in range(7):
        column.append([])
        
    soup = BeautifulSoup(r.text, 'html.parser')

    # focusing on a certain attribute
    # this table contains court info
    attr_table = {"id": "ctl00_ContentPlaceHolder1_tab1"}
    table_body = soup.find("table", attrs = attr_table)

    rows = table_body.find_all('tr')
    for i in range(15):
        cols = rows[i].find_all('td')
        for j in range(1,8):
            # if it is the first row that contains date, add year info
            if i == 0:
                column[j-1].append(str(y)+ "/" + cols[j].get_text())
            else:
                column[j-1].append(cols[j].get_text())
    columns.extend(column)


# In[183]:


badminton_3F = pd.DataFrame(columns, columns=["date", "8:00~9:00", "9:00~10:00", "10:00~11:00", "11:00~12:00", "12:00~13:00", "13:00~14:00", "14:00~15:00", "15:00~16:00", "16:00~17:00", "17:00~18:00", "18:00~19:00", "19:00~20:00", "20:00~21:00", "21:00~22:00"])


# In[189]:


badminton_3F = badminton_3F.replace("", "有場")


# # 1F羽球場

# In[137]:


import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# In[185]:


columns_f1 = []
driver = webdriver.Chrome("/Users/pengchen/Desktop/大四上/商管程設/final_project/chromedriver")


# In[186]:


for l in range(550):
    
    y = (datetime.datetime(2009, 12, 18) + datetime.timedelta(days= l * 7)).year
    m = (datetime.datetime(2009, 12, 18) + datetime.timedelta(days= l * 7)).month
    d = (datetime.datetime(2009, 12, 18) + datetime.timedelta(days= l * 7)).day
    query_date = str(y) + "/" + str(m) + "/" + str(d)
    
    if l == 0:
        url = 'https://ntupesc.ntu.edu.tw/facilities/PlaceGrd.aspx?nFlag=0&placeSeq=1&dateLst='
        url += query_date
    
        # go to badminton info page
        driver.get(url)
        
        time.sleep(0.2)
        # close div dialog
        driver.find_element_by_xpath("//span[@class='ui-button-icon ui-icon ui-icon-closethick']").click()

        time.sleep(0.2)
        # option2 is badminton court 1F
        # because 3F and 1F have the identical URL, I open the web and select the option by webdriver
        driver.find_element_by_xpath("//select[@name='ctl00$ContentPlaceHolder1$tcTab$tpValidator$DropLstPlace']/option[@value='2']").click()
        
        time.sleep(0.5)
        # click "search" button
        driver.find_element(By.ID ,("ctl00_ContentPlaceHolder1_tcTab_tpValidator_ImageButton1")).click()
    
        # close div dialog
        driver.find_element_by_xpath("//span[@class='ui-button-icon ui-icon ui-icon-closethick']").click()
        
        time.sleep(0.2)
        # send query_date "re-send"
        driver.find_element(By.ID ,("ctl00_ContentPlaceHolder1_tcTab_tpValidator_txtDateQry")).send_keys(query_date)
        
        time.sleep(0.5)
        # click "search" button
        driver.find_element(By.ID ,("ctl00_ContentPlaceHolder1_tcTab_tpValidator_ImageButton1")).click()
    
    else:
    
        # close div dialog
        driver.find_element_by_xpath("//span[@class='ui-button-icon ui-icon ui-icon-closethick']").click()
        
        time.sleep(0.2)
        # click next week
        driver.find_element(By.ID ,("ctl00_ContentPlaceHolder1_lblNextWeek")).click()
        
    
    time.sleep(0.5)
    page = driver.page_source
    soup_f1 = BeautifulSoup(page)
    
    # focusing on a certain attribute
    # this table contains court info
    attr_table = {"id": "ctl00_ContentPlaceHolder1_tab1"}
    table_body = soup_f1.find("table", attrs = attr_table)

    column = []
    for k in range(7):
        column.append([])
        
    rows = table_body.find_all('tr')
    for i in range(15):
        cols = rows[i].find_all('td')
        for j in range(1,8):
            # if it is the first row that contains date, add year info
            if i == 0:
                column[j-1].append(str(y)+ "/" + cols[j].get_text())
            else:
                column[j-1].append(cols[j].get_text())
    columns_f1.extend(column)


# In[ ]:


driver.close()


# In[189]:


badminton_1F = pd.DataFrame(columns_f1, columns=["date", "8:00~9:00", "9:00~10:00", "10:00~11:00", "11:00~12:00", "12:00~13:00", "13:00~14:00", "14:00~15:00", "15:00~16:00", "16:00~17:00", "17:00~18:00", "18:00~19:00", "19:00~20:00", "20:00~21:00", "21:00~22:00"])


# In[190]:


badminton_1F = badminton_1F.replace("", "有場")


# # 1F與3F的資料合併

# In[210]:


result = pd.merge(badminton_1F, badminton_3F, on='date', how='inner')


# In[228]:


result.to_csv("badminton_1n3F_10y.csv",index=False)

