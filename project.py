from tkinter import *
import cv2 as cv
from PIL import Image, ImageTk
import pygame
import pyaudio

root=Tk()
root.geometry("1000x700")
# Data collection tab_1

t1f1=LabelFrame(root,text="frame 1",width=500,height=700,padx=10,pady=10)

t1f2=LabelFrame(root,text="frame 2",width=500,height=200,padx=10,pady=10)

t1f3=LabelFrame(root,text="frame 3",width=500,height=500,padx=10,pady=10)

# temporory label
Label(t1f1,text="test").pack()
Label(t1f2,text="test").pack()
Label(t1f3,text="test").pack()





# tab 1 frame 1
t1f1.grid(row=0,column=0,rowspan=2,sticky="nsew",padx=4,pady=4)
# tab 1 frame 2
t1f2.grid(row=0,column=1,sticky="nsew",padx=4,pady=4)
# tab 2 frame 3
t1f3.grid(row=1,column=1,sticky="nsew",padx=4,pady=4)




root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
t1f1.grid_rowconfigure(0, weight=1)
t1f1.grid_columnconfigure(0, weight=1)
t1f2.grid_rowconfigure(0, weight=1)
t1f2.grid_columnconfigure(0, weight=1)
t1f3.grid_rowconfigure(0, weight=1)
t1f3.grid_columnconfigure(0, weight=1)\




root.mainloop()