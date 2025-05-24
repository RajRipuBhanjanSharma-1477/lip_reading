from tkinter import *
import component.constant as constant
from component import start
root=Tk()
root.title(constant.tittle)
root.geometry(constant.size)
start1=Button(root,text="start",command=lambda :start.START(root))
start1.grid(row=0,column=0)

root.mainloop()