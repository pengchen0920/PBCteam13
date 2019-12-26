import csv
import datetime
import matplotlib.pyplot as py


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
    py.pie(Value, labels = Key, autopct = '%1.1f%%')

    if searchYear == -1 and searchMonth == -1:
        py.title('近十年'+location+'各事件機率表')
    if searchYear != -1 and searchMonth == -1:
        py.title(str(searchYear)+'年全年'+location+'各事件機率表')
    if searchYear == -1 and searchMonth != -1:
        py.title('近十年'+str(searchMonth)+'月'+location+'各事件機率表')
    if searchYear != -1 and searchMonth != -1:
        py.title(str(searchYear)+'年'+str(searchMonth)+'月'+location+'各事件機率表')
    py.legend(loc = 'best')
    py.show()
    return None

# 輸入篩選區間
searchFloor = int(input('請輸入欲查詢樓層(1,3): ')) 
print('\n', '如不需篩選則輸入-1')
searchYear = int(input('請輸入欲查詢年份(2010~2019): '))
searchMonth = int(input('請輸入欲查詢月份(1~12): '))

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
firstKey , firstValue = Sort_Simplify_Data(firstType)

thirdTotal = sum(thirdType.values())  # 三樓
for key, value in thirdType.items():
    thirdType[key] = value / thirdTotal
thirdKey , thirdValue = Sort_Simplify_Data(thirdType)

# 製圖
if searchFloor == 1:
    Plot_Graph(firstKey, firstValue, '一樓')
elif searchFloor == 3:
    Plot_Graph(thirdKey, thirdValue, '三樓')
