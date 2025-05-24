from tkinter import *
from PIL import Image,ImageTk
import cv2 as cv
import numpy as np
root=Tk()
root.geometry("500x500")
turn=True
blankImage=np.zeros((500,500,3),dtype="uint8")
cv.line(blankImage,(166,0),(166,500),(255,255,255),thickness=3)
cv.line(blankImage,(332,0),(332,500),(255,255,255),thickness=3)
cv.line(blankImage,(0,166),(500,166),(255,255,255),thickness=3)
cv.line(blankImage,(0,332),(500,332),(255,255,255),thickness=3)
playerLabel=Label(root,text="player 1 turn")
playerLabel.grid(row=0,column=0)
img1=Image.fromarray(blankImage)
img1=ImageTk.PhotoImage(img1)
bimage=Label(root,image=img1)
bimage.grid(row=1,column=0,sticky="nsew")
b1=Button(bimage,text="button1",height=6,width=12,padx=1,pady=1)
b1.place(x=41,y=41,)
b2=Button(bimage,text="button2",height=6,width=12,padx=1,pady=1)
b2.place(x=207,y=41,)
b3=Button(bimage,text="button3",height=6,width=12,padx=1,pady=1)
b3.place(x=373,y=207,)
b4=Button(bimage,text="button4",height=6,width=12,padx=1,pady=1)
b4.place(x=41,y=207,)
b5=Button(bimage,text="button5",height=6,width=12,padx=1,pady=1)
b5.place(x=207,y=207,)
b6=Button(bimage,text="button6",height=6,width=12,padx=1,pady=1)
b6.place(x=373,y=41,)
b7=Button(bimage,text="button7",height=6,width=12,padx=1,pady=1)
b7.place(x=41,y=373,)
b8=Button(bimage,text="button8",height=6,width=12,padx=1,pady=1)
b8.place(x=207,y=373,)
b9=Button(bimage,text="button9",height=6,width=12,padx=1,pady=1)
b9.place(x=373,y=373,)
root.mainloop()

def but(x):
    global turn
    if turn:
        
