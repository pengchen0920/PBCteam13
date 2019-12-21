import csv
import datetime

# filename放csv網址，請自行修改
fileName = 'C:\\Users\\Asus\\Desktop\\badminton_1n3F_10y.csv'
csvfile = open(fileName, 'r', encoding='ANSI')

rows = csv.reader(csvfile)

# firstPeriod[i][j]-->一樓星期i的第j時段
firstPeriod = [[{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期一各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期二各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期三各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期四各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期五各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期六各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]]  # 星期日各時段

# thirdPeriod[i][j]-->三樓星期i的第j時段
thirdPeriod = [[{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期一各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期二各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期三各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期四各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期五各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期六各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]]  # 星期日各時段

# totalPeriod[i][j]-->union星期i的第j時段
totalPeriod = [[{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期一各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期二各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期三各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期四各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期五各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}],  # 星期六各時段
               [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]]  # 星期日各時段

# 將一樓csv內容轉成dict並存入firstPeriod list中
count = 0
for row in rows:
    # 將第1列的日期改成datetime形式，以便找出星期幾
    if count != 0:
        row[0] = datetime.datetime.strptime(row[0][:-3], '%Y/%m/%d')
        print(row)
        print(row[0].date().weekday())

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

print('\n', '============================================', '\n')

timeList = ['8:00~9:00', '9:00~10:00', '10:00~11:00', '11:00~12:00', '12:00~13:00', '13:00~14:00', '14:00~15:00', '15:00~16:00', '16:00~17:00', '17:00~18:00', '18:00~19:00', '19:00~20:00', '20:00~21:00', '21:00~22:00']
weekList = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

# 計算事件發生總次數，並以總次數計算各事件發生機率
# 星期i 時段j
for i in range(7):
    for j in range(14):

        print('\n', weekList[i], timeList[j], '\n')
        
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
