'''2017'''

import csv
import datetime
import matplotlib.pyplot as py


def Available_Count(row):
    '''將篩選完的row值按照月份及時段分類後記錄至各自的dict中
       parameter為檔案內的一個row(list)，無return值'''
    # 一樓
    for i in range(12):  # 月
        if row[0].month == i+1:
            for j in range(14):  # 時段
                if '有場' in row[j+1]:
                    if '有場' in firstPeriod[i]:
                        firstPeriod[i]['有場'] += 1
                    else:
                        firstPeriod[i]['有場'] = 1
                else:
                    if '無場' in firstPeriod[i]:
                        firstPeriod[i]['無場'] += 1
                    else:
                        firstPeriod[i]['無場'] = 1
    # 三樓
    for i in range(12):  # 月
        if row[0].month == i+1:
            for j in range(14):  # 時段
                if '有場' in row[j+15]:
                    if '有場' in thirdPeriod[i]:
                        thirdPeriod[i]['有場'] += 1
                    else:
                        thirdPeriod[i]['有場'] = 1
                else:
                    if '無場' in thirdPeriod[i]:
                        thirdPeriod[i]['無場'] += 1
                    else:
                        thirdPeriod[i]['無場'] = 1
    # union
    for i in range(12):  # 月
        if row[0].month == i+1:
            for j in range(14):  # 時段
                if '有場' in (row[j+1], row[j+15]):
                    if '有場' in totalPeriod[i]:
                        totalPeriod[i]['有場'] += 1
                    else:
                        totalPeriod[i]['有場'] = 1
                else:
                    if '無場' in totalPeriod[i]:
                        totalPeriod[i]['無場'] += 1
                    else:
                        totalPeriod[i]['無場'] = 1
    return None

# 輸入篩選區間
print('如不需篩選則輸入-1')
searchYear = int(input('請輸入欲查詢年份(2010~2019): '))

# filename放csv網址，請自行修改
fileName = 'C:\\Users\\Asus\\Desktop\\badminton_1n3F_10y_NEW.csv'
csvfile = open(fileName, 'r', encoding='ANSI')

rows = csv.reader(csvfile)

# Period[i][j]-->星期i的第j時段
firstPeriod, thirdPeriod, totalPeriod, firstData, thirdData, totalData = [] ,[] ,[] ,[] ,[] ,[]
for i in range(12):
    firstPeriod.append({'有場':0, '無場':0})
    thirdPeriod.append({'有場':0, '無場':0})
    totalPeriod.append({'有場':0, '無場':0})
    firstData.append([])
    thirdData.append([])
    totalData.append([])

# 將csv內容轉成dict並存入Period list中
count = 0
for row in rows:
    if count != 0:
        # 將第1列的日期改成datetime形式，以便找出星期幾
        row[0] = datetime.datetime.strptime(row[0][:-3], '%Y/%m/%d')

        # 將每row內容記入dict內
        if searchYear != -1:
            if row[0].year == searchYear:
                Available_Count(row)  # 計算有場機率並記錄於Period(list)中

        if searchYear == -1:
            Available_Count(row)  # 計算有場機率並記錄於Period(list)中

    count += 1

# 關檔
csvfile.close

print('\n', '============================================', '\n')

# 計算事件發生總次數，並以總次數計算各事件發生機率
# 星期i 時段j
for i in range(12):
    # 一樓
    firstNum = sum(firstPeriod[i].values())  # 星期i時段j中的事件總次數
    for key, value in firstPeriod[i].items():
        firstPeriod[i][key] = value / firstNum  # 各事件發生機率
    firstData[i].append(firstPeriod[i]['有場'])

    # 三樓
    thirdNum = sum(thirdPeriod[i].values())  # 星期i時段j中的事件總次數
    for key, value in thirdPeriod[i].items():
        thirdPeriod[i][key] = value / thirdNum  # 各事件發生機率
    thirdData[i].append(thirdPeriod[i]['有場'])

    # union
    totalNum = sum(totalPeriod[i].values())  # 星期i時段j中的事件總次數
    for key, value in totalPeriod[i].items():
        totalPeriod[i][key] = value / totalNum  # 各事件發生機率
    totalData[i].append(totalPeriod[i]['有場'])

print(firstData)
print(thirdData)
print(totalData)

month = range(1, 13)

py.plot(month, firstData, label = '一樓', marker = 'o')
py.plot(month, thirdData, label = '三樓', marker = 'o')
py.plot(month, totalData, label = 'union', marker = 'o')

py.ylim(0, 1)
py.legend(loc = 'best')
py.xlabel('Month')
py.ylabel('Court Available Percentage')
if searchYear != -1:
    py.title(str(searchYear)+'年各月份有場機率')
else:
    py.title('近十各月份有場機率')
py.show()
