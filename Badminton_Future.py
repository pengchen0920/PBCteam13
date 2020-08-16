# NOTES:
# 1. 一週內會有這樣的資訊：(9) (6) --> (left) (already booked)
# 2. (15)可能代表有十五個空場，或十五個都被租走了，我有另外透過 img 的 src 抓狀態，並用中文註記

# RULES:
# 1. 兩天內只能現場預約
# 2. 一週內可以網路預約
# 3. 8天～兩週可以知道場地資訊


# 未來兩週場地資料
# 3F羽球場

import requests
from bs4 import BeautifulSoup
import datetime

columns = []

# there will be two weeks info on web --> can flip three pages at most --> l = 3
for l in range(3):
    y = (datetime.date.today() + datetime.timedelta(days= l * 7)).year
    m = (datetime.date.today() + datetime.timedelta(days= l * 7)).month
    d = (datetime.date.today() + datetime.timedelta(days= l * 7)).day
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
            
            # if it is the first row that contains date
            if i == 0:
                column[j-1].append(cols[j].get_text())

            else:
                td_text = cols[j].get_text()
                if td_text.count("(") == 1:

                    # still needs to check
                    # if the img is green check means there are no court(15 courts are booked)
                    # else if the img is red circle means there are 15 availible court(15 courts are left)
                    # src: Image/actn010_2.gif(green check)
                    # src: Image/14dot1b.gif(red circle)

                    if cols[j].find('img').get('src') == 'Image/actn010_2.gif':
                        td_text += ":無場!"
                    elif cols[j].find('img').get('src') == 'Image/14dot1b.gif':
                         td_text += ":有場!"

                column[j-1].append(td_text)
    columns.extend(column)

start_day = str(datetime.date.today())
end_day =  str(datetime.date.today() + datetime.timedelta(days= 14))


# modify date string form to search easily

start_day = start_day.replace("-", "/")[5:]
if start_day[0] == '0':
    start_day = start_day[1:]
end_day = end_day.replace("-", "/")[5:]
if end_day[0] == '0':
    end_day = end_day[1:]

# filter columns to 14 days -> from today to 14 days after
start_pos = 0

for i in range(len(columns)):
    date = columns[i][0]
    if start_day in date:
        start_pos = i

two_weeks_3F = columns[start_pos:start_pos+15]

# within one week can be booked online
for day in two_weeks_3F[:8]:
    for time in range(1, 15):
        if ("(" in day[time] ) and ("無場" not in day[time]):
            day[time] += " 已開放網路預約"

# one week after can't be booked online
for day in two_weeks_3F[8:]:
    for time in range(1, 15):
        if ("(" in day[time] ) and ("無場" not in day[time]):
            day[time] += " 尚未開放網路預約"


# for day in two_weeks_3F:

time_table = []
for i in range(15):
    time_table.append([])

for day in range(15):
    for j in range(1,15):
        if(("有場" in two_weeks_3F[day][j]) or (two_weeks_3F[day][j].count("(") == 2)):
            time_table[day].append(1)
        else:
            time_table[day].append(0)

print(time_table)


# important note!
# (9) (6) --> (left) (already booked)

# 1F!!!!!!
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

columns_1f = []
driver = webdriver.Chrome("/Users/pengchen/Desktop/大四上/商管程設/final_project/chromedriver")

for l in range(3):
    
    y = (datetime.date.today() + datetime.timedelta(days= l * 7)).year
    m = (datetime.date.today() + datetime.timedelta(days= l * 7)).month
    d = (datetime.date.today() + datetime.timedelta(days= l * 7)).day
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
            # if it is the first row that contains date
            if i == 0:
                column[j-1].append(cols[j].get_text())
                
            else:
                td_text = cols[j].get_text()
                if td_text.count("(") == 1:
                    
                    # still needs to check
                    # if the img is green check means there are no court(15 courts are booked)
                    # else if the img is red circle means there are 15 availible court(15 courts are left)
                    # src: Image/actn010_2.gif(green check)
                    # src: Image/14dot1b.gif(red circle)
                    
                    if cols[j].find('img').get('src') == 'Image/actn010_2.gif':
                        td_text += ":無場!"
                    elif cols[j].find('img').get('src') == 'Image/14dot1b.gif':
                         td_text += ":有場!"
                
               
                column[j-1].append(td_text)
                
    columns_1f.extend(column)

start_pos_1f = 0

for i in range(len(columns_1f)):
    date = columns[i][0]
    if start_day in date:
        start_pos_1f = i
        break

two_weeks_1F = columns_1f[start_pos_1f:start_pos_1f+15]

# within one week can be booked online
for day in two_weeks_1F[:8]:
    for time in range(1, 15):
        if ("(" in day[time] ) and ("無場" not in day[time]) and ("現場訂位" not in day[time]):
            day[time] += " 已開放網路預約"

# one week after can't be booked online
for day in two_weeks_1F[8:]:
    for time in range(1, 15):
        if ("(" in day[time] ) and ("無場" not in day[time]):
            day[time] += " 尚未開放網路預約"

time_table_1f = []
for i in range(15):
    time_table_1f.append([])

for day in range(15):
    for j in range(1,15):
        if(("有場" in two_weeks_1F[day][j]) or (two_weeks_1F[day][j].count("(") == 2)):
            time_table_1f[day].append(1)
        else:
            time_table_1f[day].append(0)
