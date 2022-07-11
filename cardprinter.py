from tkinter import *
from tkinter import ttk

WINDOW_TITLE  = "SH Card Printer"
WINDOW_WIDTH  = 640
WINDOW_HEIGHT = 480 
WINDOW_X_POS  = 600
WINDOW_Y_POS  = 200

window = Tk()

frm = ttk.Frame(window, padding=10)
frm.grid()

ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=window.destroy).grid(column=1, row=0)

#Start window at the center of the screen
window.title(WINDOW_TITLE)
window.geometry('{}x{}+{}+{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_X_POS, WINDOW_Y_POS))
window.mainloop()

