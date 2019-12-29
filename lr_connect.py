import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def lr_training():
    logistic_data = pd.read_csv('logistic_data.csv')
    logistic_data = pd.get_dummies(logistic_data, columns = ["floor", "month", "weekday", "time"])

    # independent variables
    x = logistic_data[['floor_一樓', 'floor_三樓', 'month_1', 'month_2', 'month_3',
           'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9',
           'month_10', 'month_11', 'month_12', 'weekday_一', 'weekday_二', 'weekday_三',
           'weekday_四', 'weekday_五', 'weekday_六', 'weekday_日', 'time_8',
           'time_9', 'time_10', 'time_11', 'time_12', 'time_13', 'time_14',
           'time_15', 'time_16', 'time_17', 'time_18', 'time_19', 'time_20',
           'time_21']]
    # depependent variable
    y = logistic_data[['court']]

    x_train,x_test,y_train,y_test = train_test_split(x, y, test_size = 0.3, random_state = 20191225) 

    # train the lr model with 70% data
    lr = LogisticRegression()
    lr.fit(x_train,y_train)

    return lr


def lr_predict(logistic_model):
    input_floor = int(input("Enter floor:"))
    input_month = int(input("Enter month:"))
    input_weekday = int(input("Enter weekday:"))
    input_time = int(input("Enter time:"))


    input_all = [[]]
    for i in range(35):
        input_all[0].append(0)

    data_input = pd.DataFrame(input_all, columns=['floor_一樓', 'floor_三樓', 'month_1', 'month_2', 'month_3',
           'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9',
           'month_10', 'month_11', 'month_12', 'weekday_一', 'weekday_二', 'weekday_三',
           'weekday_四', 'weekday_五', 'weekday_六', 'weekday_日', 'time_8',
           'time_9', 'time_10', 'time_11', 'time_12', 'time_13', 'time_14',
           'time_15', 'time_16', 'time_17', 'time_18', 'time_19', 'time_20',
           'time_21'])

    # according to input of the user to generate input for the model
    if input_floor == 1:
        data_input.iloc[0][0] = 1
    else:
        data_input.iloc[0][1] = 1

    data_input.iloc[0][input_month + 1] = 1
    data_input.iloc[0][input_weekday + 13] = 1
    data_input.iloc[0][input_time + 13] = 1

    
    final_result = logistic_model.predict(data_input)
    predict_result_per = np.round(logistic_model.predict_proba(data_input),3)
    print("無場機率：" , predict_result_per[0][0], "/ 有場機率：", predict_result_per[0][1])

    print("最終判定", end = "")
    if final_result[0] == 0:
        print("無場！")
    else:
        print("有場！")

