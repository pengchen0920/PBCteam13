import tkinter as tk
from tkinter import ttk
 
# app = tk.Tk() 
# app.geometry('1200x1200')

# labelTop = tk.Label(app, text = "Choose your favourite month")
# labelTop.grid(column=0, row=0)

# comboExample = ttk.Combobox(app, 
#                             values=[
#                                     "January", 
#                                     "February",
#                                     "March",
#                                     "April"])
# print(dict(comboExample)) 
# comboExample.grid(column=0, row=1)
# comboExample.current(1)

# print(comboExample.current(), comboExample.get())

# app.mainloop()

OptionList = [
"純文字分析",
"有場分析_時段",
"有場分析_月",
"活動分析_時段",
"活動分析_月",
"各事件分析_時段",
"各事件分析_月"
] 

app = tk.Tk()

app.geometry('800x800')
app.title("search")

variable = tk.StringVar(app)
variable.set(OptionList[0])

tk.Label(font=('Helvetica', 18), text="歷史查詢事件").pack(side="top")
opt = tk.OptionMenu(app, variable, *OptionList)
opt.config(width=40, font=('Helvetica', 18))
opt.pack(side="top")

labelTest = tk.Label(text="", font=('Helvetica', 18), fg='red')
labelTest.pack(side="top")

def create_one():
    w = tk.Toplevel()
    w.geometry('800x800')
    w.title('result')

    # t_a = tk.Label(w, text="請輸入是否要篩選(Y/N):")
    # t_a.grid(row=0, column=0)
    # a = tk.Entry(w,width=30,fg="black")
    # a.grid(row=0, column=1)


    # def enter_event1(event):
    #     def enter_event2(event):
    #         if (b.get()):
    #             t_c = tk.Label(w, text="請輸入欲查詢時段(8~21):")
    #             t_c.grid(row=2, column=0)
    #             c = tk.Entry(w,width=30,fg="black")
    #             c.grid(row=2, column=1)
    #     if (a.get()=='y' or a.get()=='Y'):
    #         t_b = tk.Label(w, text="請輸入欲查詢星期(1~7):")
    #         t_b.grid(row=1, column=0)
    #         b = tk.Entry(w,width=30,fg="black")
    #         b.grid(row=1, column=1)
    #         b.bind("<Return>", enter_event2)

    # a.bind("<Return>", enter_event1)

def create_two():
    w = tk.Toplevel()
    w.geometry('600x600')
    w.title('result')

    t_a = tk.Label(w, text="請輸入欲查詢樓層(0,1,3) (如不需篩選則輸入-1):")
    t_a.grid(row=0, column=0)
    a = tk.Entry(w,width=30,fg="black")
    a.grid(row=0, column=1)

    def enter_event1(event):
        def enter_event2(event):
            if (b.get()):
                t_c = tk.Label(w, text="請輸入欲查詢月份(1~12):")
                t_c.grid(row=2, column=0)
                c = tk.Entry(w,width=30,fg="black")
                c.grid(row=2, column=1)
                done = tk.Button(w, text='完成', width=10, height=1, font=('Helvetica', 18), command="")
                done.grid(row=3, column=1)
        if (a.get()):
            t_b = tk.Label(w, text="請輸入欲查詢年份(2010~2019):")
            t_b.grid(row=1, column=0)
            b = tk.Entry(w,width=30,fg="black")
            b.grid(row=1, column=1)
            b.bind("<Return>", enter_event2)

    a.bind("<Return>", enter_event1)
    

def create_three():
    second = tk.Toplevel()
    second.geometry('800x800')
    second.title('result')

def create_four():
    w = tk.Toplevel()
    w.geometry('600x600')
    w.title('result')

    t_a = tk.Label(w, width="32", text="請輸入欲查詢事件:")
    t_a.grid(row=0, column=0)
    a = tk.Entry(w,width=30,fg="black")
    a.grid(row=0, column=1)

    def enter_event1(event):
        def enter_event2(event):
            def enter_event3(event):
                if (c.get()):
                    t_d = tk.Label(w, width="32", text="請輸入欲查詢月份(1~12):")
                    t_d.grid(row=3, column=0)
                    d = tk.Entry(w,width=30,fg="black")
                    d.grid(row=3, column=1)
                    done = tk.Button(w, text='完成', width=10, height=1, font=('Helvetica', 18), command="")
                    done.grid(row=4, column=1)
            if (b.get()):
                t_c = tk.Label(w, width="32", text="請輸入欲查詢年份(2010~2019):")
                t_c.grid(row=2, column=0)
                c = tk.Entry(w,width=30,fg="black")
                c.grid(row=2, column=1)
                c.bind("<Return>", enter_event3)
        if (a.get()):
            t_b = tk.Label(w, width="32", text="請輸入欲查詢樓層(0,1,3) (如不需篩選則輸入-1):")
            t_b.grid(row=1, column=0)
            b = tk.Entry(w,width=30,fg="black")
            b.grid(row=1, column=1)
            b.bind("<Return>", enter_event2)

    a.bind("<Return>", enter_event1)

def create_five():
    second = tk.Toplevel()
    second.geometry('800x800')
    second.title('result')

def create_six():
    w = tk.Toplevel()
    w.geometry('800x800')
    w.title('result')

    t_a = tk.Label(w, text="請輸入欲查詢樓層(0,1,3) (如不需篩選則輸入-1):")
    t_a.grid(row=0, column=0)
    a = tk.Entry(w,width=30,fg="black")
    a.grid(row=0, column=1)

    def enter_event1(event):
        def enter_event2(event):
            if (b.get()):
                t_c = tk.Label(w, text="請輸入欲查詢時段(8~21):")
                t_c.grid(row=2, column=0)
                c = tk.Entry(w,width=30,fg="black")
                c.grid(row=2, column=1)
                done = tk.Button(w, text='完成', width=10, height=1, font=('Helvetica', 18), command="")
                done.grid(row=3, column=1)
        if (a.get()):
            t_b = tk.Label(w, text="請輸入欲查詢星期(1~7):")
            t_b.grid(row=1, column=0)
            b = tk.Entry(w,width=30,fg="black")
            b.grid(row=1, column=1)
            b.bind("<Return>", enter_event2)

    a.bind("<Return>", enter_event1)

def create_seven():
    second = tk.Toplevel()
    second.geometry('800x800')
    second.title('result')    

def callback(*args):
    labelTest.configure(text=variable.get())
    if(variable.get()==OptionList[0]):
        finish.configure(command=create_one)
    elif(variable.get()==OptionList[1]):
        finish.configure(command=create_two)
    elif(variable.get()==OptionList[2]):
        finish.configure(command=create_three)
    elif(variable.get()==OptionList[3]):
        finish.configure(command=create_four)
    elif(variable.get()==OptionList[4]):
        finish.configure(command=create_five)
    elif(variable.get()==OptionList[5]):
        finish.configure(command=create_six)
    elif(variable.get()==OptionList[6]):
        finish.configure(command=create_seven)
    
finish = tk.Button(app, text='完成', width=10, height=1, command=callback, font=('Helvetica', 18))
finish.pack()

variable.trace("w", callback)

app.mainloop()