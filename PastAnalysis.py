import csv
import datetime
import matplotlib.pyplot as py

# 2
def Text_Analysis(dataList):

    # filename放csv網址，請自行修改
    fileName = '/Users/zizhenli/Documents/GitHub/PBCteam13/badminton_1n3F_10y.csv'
    csvfile = open(fileName, 'r', encoding='utf-8')
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

            for i in range(7):  # 星期
                if row[0].date().weekday() == i:
                    for j in range(14):  # 時段
                        # 一樓
                        if row[j+1] in firstPeriod[i][j]:
                            firstPeriod[i][j][row[j+1]] += 1
                        else:
                            firstPeriod[i][j][row[j+1]] = 1

                        # 三樓
                        if row[j+15] in thirdPeriod[i][j]:
                            thirdPeriod[i][j][row[j+15]] += 1
                        else:
                            thirdPeriod[i][j][row[j+15]] = 1

                        # union
                        if '有場' in (row[j+1], row[j+15]):
                            if '有場' in totalPeriod[i][j]:
                                totalPeriod[i][j]['有場'] += 1
                            else:
                                totalPeriod[i][j]['有場'] = 1
                        else:
                            if '無場' in totalPeriod[i][j]:
                                totalPeriod[i][j]['無場'] += 1
                            else:
                                totalPeriod[i][j]['無場'] = 1
        count += 1

    # 關檔
    csvfile.close

    '''
    # 輸入欲查詢範圍
    preciseSearch = input('請輸入是否要篩選(Y/N): ')
    if preciseSearch in('y', 'Y'):
        searchWeek = int(input('請輸入欲查詢星期(1~7): '))
        searchHour = int(input('請輸入欲查詢時段(8~21): '))
    '''
    print("1",dataList)
    print(dataList[0])

    searchWeek = dataList[0]
    searchHour = dataList[1]

    timeList = ['8:00~9:00', '9:00~10:00', '10:00~11:00', '11:00~12:00', '12:00~13:00', '13:00~14:00', '14:00~15:00', '15:00~16:00', '16:00~17:00', '17:00~18:00', '18:00~19:00', '19:00~20:00', '20:00~21:00', '21:00~22:00']
    weekList = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

    # 計算事件發生總次數，並以總次數計算各事件發生機率
    # 星期i 時段j
    for i in range(7):
        for j in range(14):
            if i == searchWeek-1 and j == searchHour-8:
                print(weekList[i], timeList[j], '\n')
                # 一樓
                total = sum(firstPeriod[i][j].values())  # 星期i時段j中的事件總次數
                for key, value in firstPeriod[i][j].items():
                    firstPeriod[i][j][key] = value / total  # 各事件發生機率
                sortedfirstPeriod = (sorted(firstPeriod[i][j].items(), key=lambda d: -d[1]))  # 按機率大小排序
                if '有場' in firstPeriod[i][j]:  # 印出有場機率
                    print('　　一樓有場機率:', '%.2f' % (firstPeriod[i][j]['有場'] * 100)+'%')
                else:
                    print('　　一樓有場機率: 0.00%')
                print()
                for k in range(5):  # 印出前五高的事件及其機率
                    print('　　　　', sortedfirstPeriod[k][0], '%.2f' % (sortedfirstPeriod[k][1] * 100)+'%')
                print()
                # 三樓
                total = sum(thirdPeriod[i][j].values())  # 星期i時段j中的事件總次數
                for key, value in thirdPeriod[i][j].items():
                    thirdPeriod[i][j][key] = value / total  # 各事件發生機率
                sortedthirdPeriod = (sorted(thirdPeriod[i][j].items(), key=lambda d: -d[1]))  # 按機率大小排序
                if '有場' in thirdPeriod[i][j]:  # 印出有場機率
                    print('　　三樓有場機率:', '%.2f' % (thirdPeriod[i][j]['有場'] * 100)+'%')
                else:
                    print('　　三樓有場機率: 0.00%')
                print()
                for k in range(5):  # 印出前五高的事件及其機率
                    print('　　　　', sortedthirdPeriod[k][0], '%.2f' % (sortedthirdPeriod[k][1] * 100)+'%')
                print()
                # union
                total = sum(totalPeriod[i][j].values())  # 星期i時段j中的事件總次數

                for key, value in totalPeriod[i][j].items():
                    totalPeriod[i][j][key] = value / total  # 各事件發生機率

                sortedTotalPeriod = (sorted(totalPeriod[i][j].items(), key=lambda d: -d[1]))  # 按機率大小排序
                if '有場' in totalPeriod[i][j]:  # 印出有場機率
                    print('　　union後有場機率:', '%.2f' % (totalPeriod[i][j]['有場'] * 100)+'%')
                else:
                    print('　　union後有場機率: 0.00%')
                print()

# 3
def Avail_Analysis_Period(dataList):


    def Available_Time_Count(row):
        '''將篩選完的row值按照星期及時段分類後記錄至各自的dict中
           parameter為檔案內的一個row(list)，無return值'''
        for i in range(7):  # 星期
            if row[0].date().weekday() == i:
                for j in range(14):  # 時段
                    # 一樓
                    if '有場' in (row[j+1]):
                        if '有場' in firstPeriod[i][j]:
                            firstPeriod[i][j]['有場'] += 1
                        else:
                            firstPeriod[i][j]['有場'] = 1
                    else:
                        if '無場' in firstPeriod[i][j]:
                            firstPeriod[i][j]['無場'] += 1
                        else:
                            firstPeriod[i][j]['無場'] = 1
                    # 三樓
                    if '有場' in (row[j+15]):
                        if '有場' in thirdPeriod[i][j]:
                            thirdPeriod[i][j]['有場'] += 1
                        else:
                            thirdPeriod[i][j]['有場'] = 1
                    else:
                        if '無場' in thirdPeriod[i][j]:
                            thirdPeriod[i][j]['無場'] += 1
                        else:
                            thirdPeriod[i][j]['無場'] = 1
                    # union
                    if '有場' in (row[j+1], row[j+15]):
                        if '有場' in totalPeriod[i][j]:
                            totalPeriod[i][j]['有場'] += 1
                        else:
                            totalPeriod[i][j]['有場'] = 1
                    else:
                        if '無場' in totalPeriod[i][j]:
                            totalPeriod[i][j]['無場'] += 1
                        else:
                            totalPeriod[i][j]['無場'] = 1
        return None


    def Plot_Graph(data, location):
        '''將整理好的資料進行作圖
           parameter為資料檔(list)以及樓層位置(str)，無return值'''
        for i in range(7):
            percent = data[i]
            py.plot(time, percent, label=weekList[i], marker='o')

        py.ylim(0, 1)
        py.legend(loc='best')
        py.xlabel('Time(hour)')
        py.ylabel('Court Available Percentage')
        if searchYear == -1 and searchMonth == -1:
            py.title('近十年'+location+'有場機率表')
        if searchYear != -1 and searchMonth == -1:
            py.title(str(searchYear)+'年全年'+location+'有場機率表')
        if searchYear == -1 and searchMonth != -1:
            py.title('近十年'+str(searchMonth)+'月'+location+'有場機率表')
        if searchYear != -1 and searchMonth != -1:
            py.title(str(searchYear)+'年'+str(searchMonth)+'月'+location+'有場機率表')
        py.show()
        return None


    '''main function'''
    '''
    # 輸入篩選區間
    searchFloor = int(input('請輸入欲查詢樓層(0,1,3): '))
    print('\n', '如不需篩選則輸入-1')
    searchYear = int(input('請輸入欲查詢年份(2010~2019): '))
    searchMonth = int(input('請輸入欲查詢月份(1~12): '))
    '''
    searchFloor = dataList[0]
    searchYear = dataList[1]
    searchMonth = dataList[2]

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
                    Available_Time_Count(row)

            # 僅篩選月
            if searchYear == -1 and searchMonth != -1:
                if row[0].month == searchMonth:
                    Available_Time_Count(row)

            # 年月皆篩選
            if searchYear != -1 and searchMonth != -1:
                if row[0].year == searchYear and row[0].month == searchMonth:
                    Available_Time_Count(row)

            # 年月皆不篩選
            if searchYear == -1 and searchMonth == -1:
                if True:
                    Available_Time_Count(row)
        count += 1

    # 關檔
    csvfile.close

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
            if '有場' in firstPeriod[i][j]:
                firstData[i].append(firstPeriod[i][j]['有場'])
            else:
                firstData[i].append(0)
            if '有場' in thirdPeriod[i][j]:
                thirdData[i].append(thirdPeriod[i][j]['有場'])
            else:
                thirdData[i].append(0)
            if '有場' in totalPeriod[i][j]:
                totalData[i].append(totalPeriod[i][j]['有場'])
            else:
                totalData[i].append(0)

    time = timeList

    # 一樓有場機率分配圖
    if searchFloor == 1:
        Plot_Graph(firstData, '一樓')

    # 三樓有場機率分配圖
    elif searchFloor == 3:
        Plot_Graph(thirdData, '三樓')

    # union有場機率分配圖
    elif searchFloor == 0:
        Plot_Graph(totalData, 'union後')

# 1
def Avail_Analysis_Month(dataList):


    def Available_Month_Count(row):
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


    '''main function'''
    '''
    # 輸入篩選區間
    print('如不需篩選則輸入-1')
    searchYear = int(input('請輸入欲查詢年份(2010~2019): '))
    '''
    searchYear = dataList[0]

    # filename放csv網址，請自行修改
    fileName = 'C:\\Users\\Asus\\Desktop\\badminton_1n3F_10y_NEW.csv'
    csvfile = open(fileName, 'r', encoding='ANSI')

    rows = csv.reader(csvfile)

    # Period[i][j]-->星期i的第j時段
    firstPeriod, thirdPeriod, totalPeriod, firstData, thirdData, totalData = [], [], [], [], [], []
    for i in range(12):
        firstPeriod.append({'有場': 0, '無場': 0})
        thirdPeriod.append({'有場': 0, '無場': 0})
        totalPeriod.append({'有場': 0, '無場': 0})
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
                    Available_Month_Count(row)  # 計算有場機率並記錄於Period(list)中

            if searchYear == -1:
                Available_Month_Count(row)  # 計算有場機率並記錄於Period(list)中

        count += 1

    # 關檔
    csvfile.close

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

    month = range(1, 13)

    py.plot(month, firstData, label='一樓', marker='o')
    py.plot(month, thirdData, label='三樓', marker='o')
    py.plot(month, totalData, label='union', marker='o')

    py.ylim(0, 1)
    py.legend(loc='best')
    py.xlabel('Month')
    py.ylabel('Court Available Percentage')
    if searchYear != -1:
        py.title(str(searchYear)+'年各月份有場機率')
    else:
        py.title('近十各月份有場機率')
    py.show()

# 4
def Single_Event_Analysis_Period(dataList):


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
    '''
    # 輸入欲查詢事件及篩選區間
    searchEvent = input('請輸入欲查詢事件: ')
    searchFloor = int(input('請輸入欲查詢樓層(0,1,3): '))
    print('\n', '如不需篩選則輸入-1')
    searchYear = int(input('請輸入欲查詢年份(2010~2019): '))
    searchMonth = int(input('請輸入欲查詢月份(1~12): '))
    '''
    searchEvent = dataList[0]
    searchFloor = dataList[1]
    searchYear = dataList[2]
    searchMonth = dataList[3]

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

# 2
def Single_Event_Analysis_Month(dataList):


    def Available_Count(row):
        '''將篩選完的row值按照月份及時段分類後記錄至各自的dict中
           parameter為檔案內的一個row(list)，無return值'''
        # 一樓
        for i in range(12):  # 月
            if row[0].month == i+1:
                for j in range(14):  # 時段
                    if searchEvent in row[j+1]:
                        if searchEvent in firstPeriod[i]:
                            firstPeriod[i][searchEvent] += 1
                        else:
                            firstPeriod[i][searchEvent] = 1
                    else:
                        if 'no event' in firstPeriod[i]:
                            firstPeriod[i]['no event'] += 1
                        else:
                            firstPeriod[i]['no event'] = 1
        # 三樓
        for i in range(12):  # 月
            if row[0].month == i+1:
                for j in range(14):  # 時段
                    if searchEvent in row[j+15]:
                        if searchEvent in thirdPeriod[i]:
                            thirdPeriod[i][searchEvent] += 1
                        else:
                            thirdPeriod[i][searchEvent] = 1
                    else:
                        if 'no event' in thirdPeriod[i]:
                            thirdPeriod[i]['no event'] += 1
                        else:
                            thirdPeriod[i]['no event'] = 1
        # union
        for i in range(12):  # 月
            if row[0].month == i+1:
                for j in range(14):  # 時段
                    if searchEvent in (row[j+1], row[j+15]):
                        if searchEvent in totalPeriod[i]:
                            totalPeriod[i][searchEvent] += 1
                        else:
                            totalPeriod[i][searchEvent] = 1
                    else:
                        if 'no event' in totalPeriod[i]:
                            totalPeriod[i]['no event'] += 1
                        else:
                            totalPeriod[i]['no event'] = 1
        return None


    '''main function'''
    '''
    # 輸入欲查詢事件及篩選區間
    searchEvent = input('請輸入欲查詢事件: ')
    print('\n'+'如不需篩選則輸入-1')
    searchYear = int(input('請輸入欲查詢年份(2010~2019): '))
    '''
    searchEvent = dataList[0]
    searchYear = dataList[1]

    # filename放csv網址，請自行修改
    fileName = 'C:\\Users\\Asus\\Desktop\\badminton_1n3F_10y_NEW.csv'
    csvfile = open(fileName, 'r', encoding='ANSI')

    rows = csv.reader(csvfile)

    # Period[i][j]-->星期i的第j時段
    firstPeriod, thirdPeriod, totalPeriod, firstData, thirdData, totalData = [], [], [], [], [], []
    for i in range(12):
        firstPeriod.append({'有場': 0, '無場': 0})
        thirdPeriod.append({'有場': 0, '無場': 0})
        totalPeriod.append({'有場': 0, '無場': 0})
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

    # 計算事件發生總次數，並以總次數計算各事件發生機率
    # 星期i 時段j
    for i in range(12):
        # 一樓
        firstNum = sum(firstPeriod[i].values())  # 星期i時段j中的事件總次數
        for key, value in firstPeriod[i].items():
            firstPeriod[i][key] = value / firstNum  # 各事件發生機率
        if searchEvent in firstPeriod[i]:
            firstData[i].append(firstPeriod[i][searchEvent])
        else:
            firstData[i].append(0)
        # 三樓
        thirdNum = sum(thirdPeriod[i].values())  # 星期i時段j中的事件總次數
        for key, value in thirdPeriod[i].items():
            thirdPeriod[i][key] = value / thirdNum  # 各事件發生機率
        if searchEvent in thirdPeriod[i]:
            thirdData[i].append(thirdPeriod[i][searchEvent])
        else:
            thirdData[i].append(0)
        # union
        totalNum = sum(totalPeriod[i].values())  # 星期i時段j中的事件總次數
        for key, value in totalPeriod[i].items():
            totalPeriod[i][key] = value / totalNum  # 各事件發生機率
        if searchEvent in totalPeriod[i]:
            totalData[i].append(totalPeriod[i][searchEvent])
        else:
            totalData[i].append(0)

    month = range(1, 13)

    py.plot(month, firstData, label='一樓', marker='o')
    py.plot(month, thirdData, label='三樓', marker='o')
    py.plot(month, totalData, label='union', marker='o')

    py.ylim(0)
    py.legend(loc='best')
    py.xlabel('Month')
    py.ylabel('Court Available Percentage')
    if searchYear != -1:
        py.title(str(searchYear)+'年各月份'+searchEvent+'發生機率表')
    else:
        py.title('近十年各月份'+searchEvent+'發生機率表')
    py.show()

# 3
def Multi_Event_Analysis_Period(dataList):

    def Event_Count(row):
        '''將篩選完的row值記錄至各自的dict中
           parameter為檔案內的一個row(list)，無return值'''
        for i in range(14):  # 每一row(天)的各時段
            if searchHour != -1:
                i = searchHour - 8
            # 一樓
            if row[i+1] in firstType:
                firstType[row[i+1]] += 1
            else:
                firstType[row[i+1]] = 1
            # 三樓
            if row[i+15] in thirdType:
                thirdType[row[i+15]] += 1
            else:
                thirdType[row[i+15]] = 1
            if searchHour != -1:
                break
        return None


    def Sort_Simplify_Data(Type):
        '''將資料排序並簡化：若event超過六個，新增其他欄
           parameter為已整理好的event data(dict)，回傳整理好的key及value(list)以便製圖'''
        Data = {}
        Key = []
        Value = []
        sortedType = (sorted(Type.items(), key=lambda d: -d[1]))  # 按機率大小排序
        if len(sortedType) > 6:
            otherSum = 0
            for i in range(5, len(sortedType)):
                otherSum += sortedType[i][1]
                sortedType[5] = ('其他', otherSum)
                Data = sortedType[:6]
            for i in range(6):
                Key.append(Data[i][0])
                Value.append(Data[i][1])
        else:
            Data = sortedType[:6]
            for i in range(len(sortedType)):
                Key.append(Data[i][0])
                Value.append(Data[i][1])
        return Key, Value


    def Plot_Graph(Key, Value, location):
        '''將結果繪製成圓餅圖
           parameter為Key, Value兩項(list)以及樓層位置(str)，無return值'''
        py.pie(Value, labels=Key, autopct='%1.1f%%')

        weekday = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

        if searchWeek == -1 and searchHour == -1:
            py.title(location+'各事件機率表')
        if searchWeek != -1 and searchHour == -1:
            py.title(weekday[searchWeek-1]+location+'各事件機率表')
        if searchWeek == -1 and searchHour != -1:
            py.title(str(searchHour)+':00~'+str(searchHour+1)+':00'+location+'各事件機率表')
        if searchWeek != -1 and searchHour != -1:
            py.title(weekday[searchWeek-1]+str(searchHour)+':00~'+str(searchHour+1)+':00'+location+'各事件機率表')
        py.legend(loc='best')
        py.show()
        return None


    '''main function'''
    '''
    # 輸入篩選區間
    searchFloor = int(input('請輸入欲查詢樓層(1,3): '))
    print('\n', '如不需篩選則輸入-1')
    searchWeek = int(input('請輸入欲查詢星期(1~7): '))
    searchHour = int(input('請輸入欲查詢時段(8~21): '))
    '''
    searchFloor = dataList[0]
    searchWeek = dataList[1]
    searchHour = dataList[2]
    
    # filename放csv網址，請自行修改
    fileName = 'C:\\Users\\Asus\\Desktop\\badminton_1n3F_10y_NEW.csv'
    csvfile = open(fileName, 'r', encoding='ANSI')

    rows = csv.reader(csvfile)

    firstType = {}
    thirdType = {}

    # 將csv內容轉成dict並存入Type list中
    count = 0
    for row in rows:
        # 將第1列的日期改成datetime形式，以便找出星期幾
        if count != 0:
            row[0] = datetime.datetime.strptime(row[0][:-3], '%Y/%m/%d')
            # 僅篩選年
            if searchWeek != -1 and searchHour == -1:
                if row[0].date().weekday() == searchWeek-1:
                    Event_Count(row)
            # 僅篩選月
            if searchWeek == -1 and searchHour != -1:
                Event_Count(row)
            # 年月皆篩選
            if searchWeek != -1 and searchHour != -1:
                if row[0].date().weekday() == searchWeek-1:
                    Event_Count(row)
            # 年月皆不篩選
            if searchWeek == -1 and searchHour == -1:
                Event_Count(row)
        count += 1

    # 關檔
    csvfile.close

    # 將資料排序並簡化
    firstTotal = sum(firstType.values())  # 一樓
    for key, value in firstType.items():
        firstType[key] = value / firstTotal
    firstKey, firstValue = Sort_Simplify_Data(firstType)

    thirdTotal = sum(thirdType.values())  # 三樓
    for key, value in thirdType.items():
        thirdType[key] = value / thirdTotal
    thirdKey, thirdValue = Sort_Simplify_Data(thirdType)

    # 製圖
    if searchFloor == 1:
        Plot_Graph(firstKey, firstValue, '一樓')
    elif searchFloor == 3:
        Plot_Graph(thirdKey, thirdValue, '三樓')

# 3
def Multi_Event_Analysis_Month(dataList):
    def Event_Count(row):
        '''將篩選完的row值記錄至各自的dict中
           parameter為檔案內的一個row(list)，無return值'''
        for j in range(14):  # 每一row(天)的各時段
            # 一樓
            if row[j+1] in firstType:
                firstType[row[j+1]] += 1
            else:
                firstType[row[j+1]] = 1

            # 三樓
            if row[j+15] in thirdType:
                thirdType[row[j+15]] += 1
            else:
                thirdType[row[j+15]] = 1
        return None


    def Sort_Simplify_Data(Type):
        '''將資料排序並簡化：若event超過六個，新增其他欄
           parameter為已整理好的event data(dict)，回傳整理好的key及value(list)以便製圖'''
        Data = {}
        Key = []
        Value = []
        sortedType = (sorted(Type.items(), key=lambda d: -d[1]))  # 按機率大小排序
        if len(sortedType) > 6:
            otherSum = 0
            for i in range(5, len(sortedType)):
                otherSum += sortedType[i][1]
                sortedType[5] = ('其他', otherSum)
                Data = sortedType[:6]
            for i in range(6):
                Key.append(Data[i][0])
                Value.append(Data[i][1])
        else:
            Data = sortedType[:6]
            for i in range(len(sortedType)):
                Key.append(Data[i][0])
                Value.append(Data[i][1])
        return Key, Value


    def Plot_Graph(Key, Value, location):
        '''將結果繪製成圓餅圖
           parameter為Key, Value兩項(list)以及樓層位置(str)，無return值'''
        py.pie(Value, labels=Key, autopct='%1.1f%%')

        if searchYear == -1 and searchMonth == -1:
            py.title('近十年'+location+'各事件機率表')
        if searchYear != -1 and searchMonth == -1:
            py.title(str(searchYear)+'年全年'+location+'各事件機率表')
        if searchYear == -1 and searchMonth != -1:
            py.title('近十年'+str(searchMonth)+'月'+location+'各事件機率表')
        if searchYear != -1 and searchMonth != -1:
            py.title(str(searchYear)+'年'+str(searchMonth)+'月'+location+'各事件機率表')
        py.legend(loc='best')
        py.show()
        return None


    '''main function'''
    '''
    # 輸入篩選區間
    searchFloor = int(input('請輸入欲查詢樓層(1,3): '))
    print('\n', '如不需篩選則輸入-1')
    searchYear = int(input('請輸入欲查詢年份(2010~2019): '))
    searchMonth = int(input('請輸入欲查詢月份(1~12): '))
    '''
    searchFloor = dataList[0]
    searchYear = dataList[1]
    searchMonth = dataList[2]

    # filename放csv網址，請自行修改
    fileName = 'C:\\Users\\Asus\\Desktop\\badminton_1n3F_10y_NEW.csv'
    csvfile = open(fileName, 'r', encoding='ANSI')

    rows = csv.reader(csvfile)

    firstType = {}
    thirdType = {}

    # 將csv內容轉成dict並存入Type list中
    count = 0
    for row in rows:
        # 將第1列的日期改成datetime形式，以便找出星期幾
        if count != 0:
            row[0] = datetime.datetime.strptime(row[0][:-3], '%Y/%m/%d')
            # 僅篩選年
            if searchYear != -1 and searchMonth == -1:
                if row[0].year == searchYear:
                    Event_Count(row)
            # 僅篩選月
            if searchYear == -1 and searchMonth != -1:
                if row[0].month == searchMonth:
                    Event_Count(row)
            # 年月皆篩選
            if searchYear != -1 and searchMonth != -1:
                if row[0].year == searchYear and row[0].month == searchMonth:
                    Event_Count(row)
            # 年月皆不篩選
            if searchYear == -1 and searchMonth == -1:
                Event_Count(row)
        count += 1

    # 關檔
    csvfile.close

    print('\n', '============================================', '\n')

    # 將資料排序並簡化
    firstTotal = sum(firstType.values())  # 一樓
    for key, value in firstType.items():
        firstType[key] = value / firstTotal
    firstKey, firstValue = Sort_Simplify_Data(firstType)

    thirdTotal = sum(thirdType.values())  # 三樓
    for key, value in thirdType.items():
        thirdType[key] = value / thirdTotal
    thirdKey, thirdValue = Sort_Simplify_Data(thirdType)

    # 製圖
    if searchFloor == 1:
        Plot_Graph(firstKey, firstValue, '一樓')
    elif searchFloor == 3:
        Plot_Graph(thirdKey, thirdValue, '三樓')

