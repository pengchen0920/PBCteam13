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
# driver = webdriver.Chrome(r"C:\Users\User\Desktop\chromedriver")
driver = webdriver.Chrome(r"/Users/zizhenli/Downloads/chromedriver")

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
        self.window.geometry('1200x1200')

        self.top_label = tk.Label(self.window, text='Choose the time occupied !', font=('System', 12))
        self.top_label.pack()

        self.hit = [[False for i in range(14)] for j in range(7)]

        # 建立frame
        self.frame = tk.Frame(self.window)
        self.frame.pack()
        self.frame_1 = tk.Frame(self.frame)
        self.frame_2 = tk.Frame(self.frame)
        self.frame_1.pack(side='top')
        self.frame_2.pack(side='bottom')

        # 建立時間標籤
        self.one = tk.Label(self.frame_1, text="08:00 - 09:00", width=10)
        self.one.grid(row=2, column=0)
        self.two = tk.Label(self.frame_1, text="09:00 - 10:00", width=10)
        self.two.grid(row=3, column=0)
        self.three = tk.Label(self.frame_1, text="10:00 - 11:00", width=10)
        self.three.grid(row=4, column=0)
        self.four = tk.Label(self.frame_1, text="11:00 - 12:00", width=10)
        self.four.grid(row=5, column=0)
        self.five = tk.Label(self.frame_1, text="12:00 - 13:00", width=10)
        self.five.grid(row=6, column=0)
        self.six = tk.Label(self.frame_1, text="13:00 - 14:00", width=10)
        self.six.grid(row=7, column=0)
        self.seven = tk.Label(self.frame_1, text="14:00 - 15:00", width=10)
        self.seven.grid(row=8, column=0)
        self.eight = tk.Label(self.frame_1, text="15:00 - 16:00", width=10)
        self.eight.grid(row=9, column=0)
        self.nine = tk.Label(self.frame_1, text="16:00 - 17:00", width=10)
        self.nine.grid(row=10, column=0)
        self.ten = tk.Label(self.frame_1, text="17:00 - 18:00", width=10)
        self.ten.grid(row=11, column=0)
        self.ele = tk.Label(self.frame_1, text="18:00 - 19:00", width=10)
        self.ele.grid(row=12, column=0)
        self.tew = tk.Label(self.frame_1, text="19:00 - 20:00", width=10)
        self.tew.grid(row=13, column=0)
        self.thir = tk.Label(self.frame_1, text="20:00 - 21:00", width=10)
        self.thir.grid(row=14, column=0)
        self.fourt = tk.Label(self.frame_1, text="21:00 - 22:00", width=10)
        self.fourt.grid(row=15, column=0)

        self.weekday = [None for i in range(7)]
        self.fifteen_days = [None for i in range(15)]

        # 建立 Button and result list
        self.time_button = [[None for i in range(14)] for j in range(7)]
        self.result_button = [[None for i in range(14)] for j in range(15)]

        # 建立新視窗按鈕
        # self.create = tk.Button(self.frame_2, text='OK!', bg='gray80', font=('System', 12), width=7, height=1, command=self.create)
        # self.create.pack(side='bottom')

        # 建立關閉按鈕
        self.close_button = tk.Button(self.frame_2, text='OK!', bg='gray80', font=('System', 12), width=3, height=1,
                                      command=self.close_window)
        self.close_button.pack(side='bottom')

    def create_fifteen_days(self, content):
        for i in range(15):
            self.fifteen_days[i] = tk.Label(self.frame_1, text=content[i], width=5, font=('System', 12))
            self.fifteen_days[i].grid(row=1, column=i + 1)

    def create_weekday(self, content):
        for i in range(7):
            self.weekday[i] = tk.Label(self.frame_1, text=content[i], width=5, font=('System', 12))
            self.weekday[i].grid(row=1, column=i + 1)

    def create_button(self):
        for i in range(7):
            for j in range(14):

<< << << < HEAD
self.time_button[i][j] = tk.Button(self.frame_1, text='O', bg='spring green', font=('System', 12),
                                   width=5, command=functools.partial(self.time_hit, i, j))
self.time_button[i][j].grid(row=j + 2, column=i + 1, padx=0)
== == == =
self.time_result[i][j] = tk.Label(self.frame_2, text='O', bg='spring green', font=('System', 12),
                                  width=3, height=1)
self.time_result[i][j].grid(row=j, column=i, padx=1, pady=1, ipadx=5, ipady=5)


# 跳出第二視窗
def create(self):
    second = tk.Toplevel()
    second.geometry('800x800')
    second.title('Python')

    one = tk.Label(second, text="08:00 - 09:00", width=10)
    one.grid(row=2, column=0)
    two = tk.Label(second, text="09:00 - 10:00", width=10)
    two.grid(row=3, column=0)
    three = tk.Label(second, text="10:00 - 11:00", width=10)
    three.grid(row=4, column=0)
    four = tk.Label(second, text="11:00 - 12:00", width=10)
    four.grid(row=5, column=0)
    five = tk.Label(second, text="12:00 - 13:00", width=10)
    five.grid(row=6, column=0)
    six = tk.Label(second, text="13:00 - 14:00", width=10)
    six.grid(row=7, column=0)
    seven = tk.Label(second, text="14:00 - 15:00", width=10)
    seven.grid(row=8, column=0)
    eight = tk.Label(second, text="15:00 - 16:00", width=10)
    eight.grid(row=9, column=0)
    nine = tk.Label(second, text="16:00 - 17:00", width=10)
    nine.grid(row=10, column=0)
    ten = tk.Label(second, text="17:00 - 18:00", width=10)
    ten.grid(row=11, column=0)
    ele = tk.Label(second, text="18:00 - 19:00", width=10)
    ele.grid(row=12, column=0)
    tew = tk.Label(second, text="19:00 - 20:00", width=10)
    tew.grid(row=13, column=0)
    thir = tk.Label(second, text="20:00 - 21:00", width=10)
    thir.grid(row=14, column=0)
    fourt = tk.Label(second, text="21:00 - 22:00", width=10)
    fourt.grid(row=15, column=0)

    a = tk.Label(second, text="星期一", width=10)
    a.grid(row=1, column=1)
    b = tk.Label(second, text="星期二", width=10)
    b.grid(row=1, column=2)
    c = tk.Label(second, text="星期三", width=10)
    c.grid(row=1, column=3)
    d = tk.Label(second, text="星期四", width=10)
    d.grid(row=1, column=4)
    e = tk.Label(second, text="星期五", width=10)
    e.grid(row=1, column=5)
    f = tk.Label(second, text="星期六", width=10)
    f.grid(row=1, column=6)
    g = tk.Label(second, text="星期日", width=10)
    g.grid(row=1, column=7)

    height = 14
    width = 7
    for i in range(2, height + 2):  # Rows
        for j in range(1, width + 1):  # Columns
            blank = tk.Button(second, width=10, highlightbackground='LemonChiffon')
            blank.grid(row=i, column=j)

>> >> >> > 4
f20476cdac77527c2dd517d9c5c6e9c1b319165


def create_result(self, content):
    for i in range(15):
        for j in range(14):
            self.result_button[i][j] = tk.Button(self.frame_1, text=content[i][j], bg='spring green',
                                                 font=('System', 12), width=5,
                                                 command=functools.partial(self.time_hit, i, j))
            self.result_button[i][j].grid(row=j + 2, column=i + 1, padx=0)


def time_hit(self, i, j):
    if not self.hit[i][j]:
        self.hit[i][j] = True
        self.time_button[i][j].configure(bg='orange red', text='X')
    else:
        self.hit[i][j] = False
        self.time_button[i][j].configure(bg='spring green', text='O')


def close_window(self):
    self.window.destroy()


weekday = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

# 主程式執行
window1 = Window()
window1.create_weekday(weekday)
window1.create_button()
window1.window.mainloop()

# 將點擊資料轉換成有空的時間
time_available = []
for i in range(7):
    time_available.append([])
    for j in range(14):
        time_available[i].append(int(not window1.hit[i][j]))

'''
print('-'*50)
print('0 for occupied, 1 for available.')
print('-'*50)
print('print time_available')
for i in range(7):
    print('Weekday %d : ' %(i+1), time_available[i])
'''

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
        weekday_temp = weekday_today % 7
        if time_available[weekday_temp][j] == 1 and (time_table[i][j] == 1 or time_table_1f[i][j] == 1):
            time_final[i][j] = 1
    weekday_today += 1

# 印出結果
date_today = datetime.date.today()
date_today1 = datetime.date.today()
fifteen_days = []
for i in range(15):
    fifteen_days.append(date_today.strftime('%m/%d'))
    date_today += datetime.timedelta(days=1)

'''
print('-'*50)
print('print time_final')
for i in range(15):
    print('%s : ' %(date_today.strftime('%Y/%m/%d')), time_final[i])
    date_today += datetime.timedelta(days=1)
'''

# 疊合過後之剩餘可借場地數量
final_room = []
for i in range(15):
    final_room.append([])
    for j in range(14):
        if time_final[i][j] == 0:
            final_room[i].append('x')
        else:
            beg = two_weeks_1F[i][j + 1].find('(')
            end = two_weeks_1F[i][j + 1].find(')')
            final_room[i].append(two_weeks_1F[i][j + 1][beg:end + 1])
            if two_weeks_1F[i][j + 1][beg:end + 1] == '':
                final_room[i][j] += '(0)'
            beg = two_weeks_3F[i][j + 1].find('(')
            end = two_weeks_3F[i][j + 1].find(')')
            final_room[i][j] += two_weeks_3F[i][j + 1][beg:end + 1]
            if two_weeks_3F[i][j + 1][beg:end + 1] == '':
                final_room[i][j] += '(0)'

'''
print('-'*50)
print('Below is the time you can book the badminton court in your available time!')
for i in range(15):
    if any(time_final[i]):
        print('%s : ' % (date_today1.strftime('%Y/%m/%d')), final_room[i])
    date_today1 += datetime.timedelta(days=1)
'''

# print(two_weeks_1F)
# print(two_weeks_3F)

window2 = Window()
window2.top_label.configure(text='This is the room you can book in your available time!')
window2.create_fifteen_days(fifteen_days)
window2.create_result(final_room)
window2.window.mainloop()
