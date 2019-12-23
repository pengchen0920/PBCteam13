import tkinter as tk

master = tk.Tk()

one = tk.Label(master, text="08:00 - 09:00", width=10)
one.grid(row=2, column=0)
two = tk.Label(master, text="09:00 - 10:00", width=10)
two.grid(row=3, column=0)
three = tk.Label(master, text="10:00 - 11:00", width=10)
three.grid(row=4, column=0)
four = tk.Label(master, text="11:00 - 12:00", width=10)
four.grid(row=5, column=0)
five = tk.Label(master, text="12:00 - 13:00", width=10)
five.grid(row=6, column=0)
six = tk.Label(master, text="13:00 - 14:00", width=10)
six.grid(row=7, column=0)
seven = tk.Label(master, text="14:00 - 15:00", width=10)
seven.grid(row=8, column=0)
eight = tk.Label(master, text="15:00 - 16:00", width=10)
eight.grid(row=9, column=0)
nine = tk.Label(master, text="16:00 - 17:00", width=10)
nine.grid(row=10, column=0)
ten = tk.Label(master, text="17:00 - 18:00", width=10)
ten.grid(row=11, column=0)
ele = tk.Label(master, text="18:00 - 19:00", width=10)
ele.grid(row=12, column=0)
tew = tk.Label(master, text="19:00 - 20:00", width=10)
tew.grid(row=13, column=0)
thir = tk.Label(master, text="20:00 - 21:00", width=10)
thir.grid(row=14, column=0)
fourt = tk.Label(master, text="21:00 - 22:00", width=10)
fourt.grid(row=15, column=0)

a = tk.Label(master, text="星期一", width=10)
a.grid(row=1, column=1)
b = tk.Label(master, text="星期二", width=10)
b.grid(row=1, column=2)
c = tk.Label(master, text="星期三", width=10)
c.grid(row=1, column=3)
d = tk.Label(master, text="星期四", width=10)
d.grid(row=1, column=4)
e = tk.Label(master, text="星期五", width=10)
e.grid(row=1, column=5)
f = tk.Label(master, text="星期六", width=10)
f.grid(row=1, column=6)
g = tk.Label(master, text="星期日", width=10)
g.grid(row=1, column=7)

height = 14
width = 7
def callback():
    print("click!")
def change_color(button):
    row    = button.grid_info()['row']
    column = button.grid_info()['column']
    print("Grid position of 'btn': {} {}".format(row, column))
    button.configure(highlightbackground='SkyBlue')
for i in range(2, height+2): #Rows
    for j in range(1, width+1): #Columns
        blank = tk.Button(master, width=10, highlightbackground='LemonChiffon')
        blank.configure(command=lambda button=blank: change_color(button))
        blank.grid(row=i, column=j)
        


tk.mainloop()