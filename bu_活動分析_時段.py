import csv
import datetime
import matplotlib.pyplot as py


def Available_Count(row):
    '''將篩選完的row值按照星期及時段分類後記錄至各自的dict中
       parameter為檔案內的一個row(list)，無return值'''
    for i in range(7):  # 星期
        if row[0].date().weekday() == i:
            for j in range(14):  # 時段
                # 一樓
                if searchEvent in (row[j+1]):
                    if searchEvent in firstPeriod[i][j]:
                        firstPeriod[i][j][searchEvent] += 1
                    else:
                        firstPeriod[i][j][searchEvent] = 1
                else:
                    if 'others' in firstPeriod[i][j]:
                        firstPeriod[i][j]['others'] += 1
                    else:
                        firstPeriod[i][j]['others'] = 1
                # 三樓
                if searchEvent in (row[j+15]):
                    if searchEvent in thirdPeriod[i][j]:
                        thirdPeriod[i][j][searchEvent] += 1
                    else:
                        thirdPeriod[i][j][searchEvent] = 1
                else:
                    if 'others' in thirdPeriod[i][j]:
                        thirdPeriod[i][j]['others'] += 1
                    else:
                        thirdPeriod[i][j]['others'] = 1
                # union
                if searchEvent in (row[j+1], row[j+15]):
                    if searchEvent in totalPeriod[i][j]:
                        totalPeriod[i][j][searchEvent] += 1
                    else:
                        totalPeriod[i][j][searchEvent] = 1
                else:
                    if 'others' in totalPeriod[i][j]:
                        totalPeriod[i][j]['others'] += 1
                    else:
                        totalPeriod[i][j]['others'] = 1
    return None


def Plot_Graph(data, location):
    '''將整理好的資料進行作圖
       parameter為資料檔(list)以及樓層位置(str)，無return值'''
    for i in range(7):
        percent = data[i]
        py.plot(time, percent, label=weekList[i], marker='o')

    py.ylim(0)
    py.legend(loc='best')
    py.xlabel('Time(hour)')
    py.ylabel('Court Available Percentage')
    if searchYear == -1 and searchMonth == -1:
        py.title('近十年'+location+searchEvent+'發生機率表')
    if searchYear != -1 and searchMonth == -1:
        py.title(str(searchYear)+'年全年'+location+searchEvent+'發生機率表')
    if searchYear == -1 and searchMonth != -1:
        py.title('近十年'+str(searchMonth)+'月'+location+searchEvent+'發生機率表')
    if searchYear != -1 and searchMonth != -1:
        py.title(str(searchYear)+'年'+str(searchMonth)+'月'+location+searchEvent+'發生機率表')
    py.show()
    return None


'''main function'''
# 輸入欲查詢事件及篩選區間
searchEvent = input('請輸入欲查詢事件: ')
searchFloor = int(input('請輸入欲查詢樓層(0,1,3): '))
print('\n', '如不需篩選則輸入-1')
searchYear = int(input('請輸入欲查詢年份(2010~2019): '))
searchMonth = int(input('請輸入欲查詢月份(1~12): '))

# filename放csv網址，請自行修改
fileName = 'C:\\Users\\Asus\\Desktop\\badminton_1n3F_10y_NEW.csv'
csvfile = open(fileName, 'r', encoding='ANSI')

rows = csv.reader(csvfile)

# Period[i][j]-->一樓星期i的第j時段
firstPeriod, thirdPeriod, totalPeriod = [], [], []
for i in range(7):
    firstPeriod.append([])
    thirdPeriod.append([])
    totalPeriod.append([])
    for j in range(14):
        firstPeriod[i].append({})
        thirdPeriod[i].append({})
        totalPeriod[i].append({})

# 將一樓csv內容轉成dict並存入firstPeriod list中
count = 0
for row in rows:
    if count != 0:
        # 將第1列的日期改成datetime形式，以便找出星期幾
        row[0] = datetime.datetime.strptime(row[0][:-3], '%Y/%m/%d')

        # 僅篩選年
        if searchYear != -1 and searchMonth == -1:
            if row[0].year == searchYear:
                Available_Count(row)

        # 僅篩選月
        if searchYear == -1 and searchMonth != -1:
            if row[0].month == searchMonth:
                Available_Count(row)

        # 年月皆篩選
        if searchYear != -1 and searchMonth != -1:
            if row[0].year == searchYear and row[0].month == searchMonth:
                Available_Count(row)

        # 年月皆不篩選
        if searchYear == -1 and searchMonth == -1:
            if True:
                Available_Count(row)
    count += 1

# 關檔
csvfile.close

print('\n', '============================================', '\n')

weekList = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
timeList = ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']

firstData = [[], [], [], [], [], [], []]
thirdData = [[], [], [], [], [], [], []]
totalData = [[], [], [], [], [], [], []]

# 計算事件發生總次數，並以總次數計算各事件發生機率
# 星期i 時段j
for i in range(7):
    for j in range(14):

        # 一樓
        total = sum(firstPeriod[i][j].values())  # 星期i時段j中的事件總次數
        for key, value in firstPeriod[i][j].items():
            firstPeriod[i][j][key] = value / total  # 各事件發生機率
        # 三樓
        total = sum(thirdPeriod[i][j].values())  # 星期i時段j中的事件總次數
        for key, value in thirdPeriod[i][j].items():
            thirdPeriod[i][j][key] = value / total  # 各事件發生機率
        # union
        total = sum(totalPeriod[i][j].values())  # 星期i時段j中的事件總次數
        for key, value in totalPeriod[i][j].items():
            totalPeriod[i][j][key] = value / total  # 各事件發生機率

        # 製圖用data
        if searchEvent in firstPeriod[i][j]:
            firstData[i].append(firstPeriod[i][j][searchEvent])
        else:
            firstData[i].append(0)
        if searchEvent in thirdPeriod[i][j]:
            thirdData[i].append(thirdPeriod[i][j][searchEvent])
        else:
            thirdData[i].append(0)
        if searchEvent in totalPeriod[i][j]:
            totalData[i].append(totalPeriod[i][j][searchEvent])
        else:
            totalData[i].append(0)

print(firstData)
print(thirdData)
print(totalData)

time = timeList

# 一樓event機率分配圖
if searchFloor == 1:
    Plot_Graph(firstData, '一樓')

# 三樓event機率分配圖
elif searchFloor == 3:
    Plot_Graph(thirdData, '三樓')

# unionevent機率分配圖
elif searchFloor == 0:
    Plot_Graph(totalData, 'union後')
