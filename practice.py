import tkinter as tk

master = tk.Tk()

a = tk.Label(master, text="星期一", width=10)
a.grid(row=1, column=0)
b = tk.Label(master, text="星期二", width=10)
b.grid(row=1, column=1)
c = tk.Label(master, text="星期三", width=10)
c.grid(row=1, column=2)
d = tk.Label(master, text="星期四", width=10)
d.grid(row=1, column=3)
e = tk.Label(master, text="星期五", width=10)
e.grid(row=1, column=4)
f = tk.Label(master, text="星期六", width=10)
f.grid(row=1, column=5)
g = tk.Label(master, text="星期日", width=10)
g.grid(row=1, column=6)

height = 14
width = 7
def callback():
    print("click!")
def change_color(button):
    row    = button.grid_info()['row']
    column = button.grid_info()['column']
    print("Grid position of 'btn': {} {}".format(row, column))
    button.configure(highlightbackground='SkyBlue')
for i in range(2, height): #Rows
    for j in range(width): #Columns
        blank = tk.Button(master, width=10, highlightbackground='LemonChiffon')
        blank.configure(command=lambda button=blank: change_color(button))
        blank.grid(row=i, column=j)
        


tk.mainloop()