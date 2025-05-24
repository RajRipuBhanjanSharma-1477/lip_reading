from tkinter import *
from tkinter import ttk
from component.tab1 import Tab1
from component.tab2 import Tab2
from component.tab3 import Tab3
import component.constant as constant
def START(root):
    tab=ttk.Notebook(root)
    tab1=Tab1(tab)
    tab2=Tab2(tab)
    tab3=Tab3(tab)
    tab.add(tab1,text=constant.s1)
    tab.add(tab2,text=constant.s2)
    tab.add(tab3,text=constant.s3)
    tab.grid(row=0,column=0,sticky="nsew")
    root.grid_rowconfigure(0,weight=1)
    root.grid_columnconfigure(0,weight=1)