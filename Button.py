# -*- coding: utf-8 -*-
import tkinter as tk
import functools

# 設定視窗
window = tk.Tk()
window.title('Time Selection')
window.geometry('800x600')
window.configure(background='white')

top_label = tk.Label(window, text='Choose the time occupied !', bg='white', font=('System', 12))
top_label.pack()

hit = [[False for i in range(10)] for j in range(5)]
# print(hit)


def time_hit(i, j):
    global hit
    if not hit[i][j]:
        hit[i][j] = True
        time_result[i][j].configure(bg='red', text='X')
    else:
        hit[i][j] = False
        time_result[i][j].configure(bg='green', text='O')


# 建立frame
frame = tk.Frame(window)
frame.pack()
frame_1 = tk.Frame(frame)
frame_2 = tk.Frame(frame)
frame_1.pack(side='left')
frame_2.pack(side='right')

# 建立button
time_button = [[None for i in range(10)] for j in range(5)]
time_result = [[None for i in range(10)] for j in range(5)]

for i in range(5):
    for j in range(10):
        time_button[i][j] = tk.Button(frame_1, text='', bg='green', font=('System', 12),
                                      width=3, height=1, command=functools.partial(time_hit, i, j))
        time_button[i][j].grid(row=j, column=i, padx=5, pady=5, ipadx=5, ipady=5)

# 建立選擇後的狀態
for i in range(5):
    for j in range(10):
        time_result[i][j] = tk.Label(frame_2, text='O', bg='green', font=('System', 12), width=4, height=1)
        time_result[i][j].grid(row=j, column=i, padx=5, pady=5, ipadx=5, ipady=5)

window.mainloop()
# print(hit)

time_available = hit
for i in range(5):
    for j in range(10):
        if time_available[i][j]:
            time_available[i][j] = 0
        else:
            time_available[i][j] = 1

print('-'*50)
print('0 for occupied, 1 for available.')
print('-'*50)
for i in range(5):
    print('Weekday %d : ' %(i+1), time_available[i])
