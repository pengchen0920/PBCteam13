# -*- coding: utf-8 -*-
import tkinter as tk
import functools

# NOTES:
# 一週內會有這樣的資訊：(9) (6) --> (left) (already booked)
# (15)可能代表有十五個空場，或十五個都被租走了，我有另外透過img的src抓狀態，並用中文註記

# 兩天內只能現場預約
# 一週內可以網路預約
# 8天～兩週可以知道場地資訊


# # 未來兩週場地資料

# ## 3F羽球場

# In[1]:


import requests
from bs4 import BeautifulSoup
import datetime

# In[62]:


columns = []
print('loading...')

# In[63]:


# there will be two weeks info on web --> can flip three pages at most --> l = 3
for l in range(3):
    y = (datetime.date.today() + datetime.timedelta(days=l * 7)).year
    m = (datetime.date.today() + datetime.timedelta(days=l * 7)).month
    d = (datetime.date.today() + datetime.timedelta(days=l * 7)).day
    query_date = str(y) + "/" + str(m) + "/" + str(d)

    url = 'https://ntupesc.ntu.edu.tw/facilities/PlaceGrd.aspx?nFlag=0&placeSeq=1&dateLst='
    url += query_date
    r = requests.get(url)

    if r.status_code == requests.codes.ok:  # OK!
        # print("OK!" + str(l + 1))
        pass

    column = []
    for k in range(7):
        column.append([])

    soup = BeautifulSoup(r.text, 'html.parser')

    # focusing on a certain attribute
    # this table contains court info
    attr_table = {"id": "ctl00_ContentPlaceHolder1_tab1"}
    table_body = soup.find("table", attrs=attr_table)

    rows = table_body.find_all('tr')
    for i in range(15):
        cols = rows[i].find_all('td')
        for j in range(1, 8):
            # if it is the first row that contains date
            if i == 0:
                column[j - 1].append(cols[j].get_text())

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

                column[j - 1].append(td_text)

    columns.extend(column)

# In[64]:


start_day = str(datetime.date.today())
end_day = str(datetime.date.today() + datetime.timedelta(days=14))

# In[65]:


# modify date string form to search easily

start_day = start_day.replace("-", "/")[5:]
if start_day[0] == '0':
    start_day = start_day[1:]
end_day = end_day.replace("-", "/")[5:]
if end_day[0] == '0':
    end_day = end_day[1:]

# In[66]:


# filter columns to 14 days -> from today to 14 days after
start_pos = 0

for i in range(len(columns)):
    date = columns[i][0]
    if start_day in date:
        start_pos = i

# In[67]:


two_weeks_3F = columns[start_pos:start_pos + 15]

# In[68]:


# within one week can be booked online
for day in two_weeks_3F[:8]:
    for time in range(1, 15):
        if ("(" in day[time]) and ("無場" not in day[time]):
            day[time] += " 已開放網路預約"

# In[69]:


# one week after can't be booked online
for day in two_weeks_3F[8:]:
    for time in range(1, 15):
        if ("(" in day[time]) and ("無場" not in day[time]):
            day[time] += " 尚未開放網路預約"

# for day in two_weeks_3F:
#     print(day)
#     print()

time_table = []
for i in range(15):
    time_table.append([])

for day in range(15):
    for j in range(1, 15):
        if (("有場" in two_weeks_3F[day][j]) or (two_weeks_3F[day][j].count("(") == 2)):
            time_table[day].append(1)
        else:
            time_table[day].append(0)

# print(time_table)

# important note!
# (9) (6) --> (left) (already booked)


# 1F!!!!!!

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# In[58]:


columns_1f = []
driver = webdriver.Chrome(r"C:\Users\User\Desktop\chromedriver")

# In[59]:


for l in range(3):

    y = (datetime.date.today() + datetime.timedelta(days=l * 7)).year
    m = (datetime.date.today() + datetime.timedelta(days=l * 7)).month
    d = (datetime.date.today() + datetime.timedelta(days=l * 7)).day
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
        driver.find_element_by_xpath(
            "//select[@name='ctl00$ContentPlaceHolder1$tcTab$tpValidator$DropLstPlace']/option[@value='2']").click()

        time.sleep(0.5)
        # click "search" button
        driver.find_element(By.ID, ("ctl00_ContentPlaceHolder1_tcTab_tpValidator_ImageButton1")).click()

        # close div dialog
        driver.find_element_by_xpath("//span[@class='ui-button-icon ui-icon ui-icon-closethick']").click()

        time.sleep(0.2)
        # send query_date "re-send"
        driver.find_element(By.ID, ("ctl00_ContentPlaceHolder1_tcTab_tpValidator_txtDateQry")).send_keys(query_date)

        time.sleep(0.5)
        # click "search" button
        driver.find_element(By.ID, ("ctl00_ContentPlaceHolder1_tcTab_tpValidator_ImageButton1")).click()

    else:

        # close div dialog
        driver.find_element_by_xpath("//span[@class='ui-button-icon ui-icon ui-icon-closethick']").click()

        time.sleep(0.2)
        # click next week
        driver.find_element(By.ID, ("ctl00_ContentPlaceHolder1_lblNextWeek")).click()

    time.sleep(0.5)
    page = driver.page_source
    soup_f1 = BeautifulSoup(page, features="html.parser")

    # focusing on a certain attribute
    # this table contains court info
    attr_table = {"id": "ctl00_ContentPlaceHolder1_tab1"}
    table_body = soup_f1.find("table", attrs=attr_table)

    column = []
    for k in range(7):
        column.append([])

    rows = table_body.find_all('tr')
    for i in range(15):
        cols = rows[i].find_all('td')
        for j in range(1, 8):
            # if it is the first row that contains date
            if i == 0:
                column[j - 1].append(cols[j].get_text())

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

                column[j - 1].append(td_text)

    columns_1f.extend(column)

# In[61]:

driver.close()
start_pos_1f = 0

for i in range(len(columns_1f)):
    date = columns[i][0]
    if start_day in date:
        start_pos_1f = i
        break

# In[63]:


two_weeks_1F = columns_1f[start_pos_1f:start_pos_1f + 15]

# In[65]:


# within one week can be booked online
for day in two_weeks_1F[:8]:
    for time in range(1, 15):
        if ("(" in day[time]) and ("無場" not in day[time]) and ("現場訂位" not in day[time]):
            day[time] += " 已開放網路預約"

# In[67]:


# one week after can't be booked online
for day in two_weeks_1F[8:]:
    for time in range(1, 15):
        if ("(" in day[time]) and ("無場" not in day[time]):
            day[time] += " 尚未開放網路預約"

# In[69]:


time_table_1f = []
for i in range(15):
    time_table_1f.append([])

# In[70]:


for day in range(15):
    for j in range(1, 15):
        if ("有場" in two_weeks_1F[day][j]) or (two_weeks_1F[day][j].count("(") == 2):
            time_table_1f[day].append(1)
        else:
            time_table_1f[day].append(0)

# print(time_table_1f)

# 這裡開始是視窗的部分


class Window:

    def __init__(self):

        # 設定視窗
        self.window = tk.Tk()
        self.window.title('Time Selection')
        self.window.geometry('800x800')
        self.window.configure(background='white')

        self.top_label = tk.Label(self.window, text='Choose the time occupied !', bg='white', font=('System', 12))
        self.top_label.pack()

        self.hit = [[False for i in range(14)] for j in range(7)]

        # 建立frame
        self.frame = tk.Frame(self.window, bg='gray99')
        self.frame.pack()
        self.frame_1 = tk.Frame(self.frame, bg='gray99')
        self.frame_2 = tk.Frame(self.frame, bg='gray99')
        self.frame_3 = tk.Frame(self.frame, bg='gray99')
        self.frame_1.pack(side='left')
        self.frame_2.pack(side='right')
        self.frame_3.pack(side='bottom')

        # 建立關閉按鈕
        self.close_button = tk.Button(self.frame_3, text='OK!', bg='gray80', font=('System', 12), width=3, height=1,
                                      command=self.close_window)
        self.close_button.pack(side='bottom')

        # 建立button & result
        self.time_button = [[None for i in range(14)] for j in range(7)]
        self.time_result = [[None for i in range(14)] for j in range(7)]

        for i in range(7):
            for j in range(14):
                self.time_button[i][j] = tk.Button(self.frame_1, text='', bg='gray80', font=('System', 12),
                                              width=3, height=1,
                                              command=functools.partial(self.time_hit, i, j), bd=0)
                self.time_button[i][j].grid(row=j, column=i, padx=1, pady=1, ipadx=5, ipady=5)

        # 建立選擇後的狀態
        for i in range(7):
            for j in range(14):
                self.time_result[i][j] = tk.Label(self.frame_2, text='O', bg='spring green', font=('System', 12), width=3,
                                             height=1)
                self.time_result[i][j].grid(row=j, column=i, padx=1, pady=1, ipadx=5, ipady=5)

    def time_hit(self, i, j):
        if not self.hit[i][j]:
            self.hit[i][j] = True
            self.time_result[i][j].configure(bg='orange red', text='X')
        else:
            self.hit[i][j] = False
            self.time_result[i][j].configure(bg='spring green', text='O')

    def close_window(self):
        self.window.destroy()


window1 = Window()
window1.window.mainloop()

# 將點擊資料轉換成有空的時間
time_available = []
for i in range(7):
    time_available.append([])
    for j in range(14):
        time_available[i].append(int(not window1.hit[i][j]))

print('-'*50)
print('0 for occupied, 1 for available.')
print('-'*50)
print('print time_available')
for i in range(7):
    print('Weekday %d : ' %(i+1), time_available[i])


# 建立最終時間表(有空以及有場(包含1 or 3))
time_final = []
for i in range(15):
    time_final.append([])
    for j in range(14):
        time_final[i].append(0)

# 疊合有空以及有場
weekday_today = datetime.date.today().weekday()
for i in range(15):
    for j in range(14):
        weekday_temp = weekday_today%7
        if time_available[weekday_temp][j] == 1 and (time_table[i][j] == 1 or time_table_1f[i][j] == 1):
            time_final[i][j] = 1
    weekday_today += 1
'''
print('-'*50)
print('print time_table')
for i in range(15):
    print('Weekday %d : ' %(i+1), time_table[i])

print('-'*50)
print('print time_table_1f')
for i in range(15):
    print('Weekday %d : ' %(i+1), time_table_1f[i])
'''
# 印出結果
date_today = datetime.date.today()
date_today1 = datetime.date.today()


print('-'*50)
print('print time_final')
for i in range(15):
    print('%s : ' %(date_today.strftime('%Y/%m/%d')), time_final[i])
    date_today += datetime.timedelta(days=1)


# 疊合過後之剩餘可借場地數量
final_room = []
for i in range(15):
    final_room.append([])
    for j in range(14):
        final_room[i].append(time_final[i][j])

for i in range(15):
    for j in range(14):
        if final_room[i][j] != 0:
            final_room[i][j] = 2

print('-'*50)
print('Below is the time you can book the badminton court in your available time!')
for i in range(15):
    if any(time_final[i]):
        print('%s : ' % (date_today1.strftime('%Y/%m/%d')), time_final[i])
    date_today1 += datetime.timedelta(days=1)

print(two_weeks_1F)
print(final_room)
