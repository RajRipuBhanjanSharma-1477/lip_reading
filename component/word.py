from tkinter import *
import component.constant as constant
import os
import cv2 as cv
import numpy as np
from PIL import Image,ImageTk
class Word(LabelFrame):
    def __init__(self,parent):
        super().__init__(parent)
        constant.word=Label(self,text="this the word",bg="#ed1bb9")
        constant.word.place(x=0,y=0,relheight=1,relwidth=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
def display_word():
    if not os.path.exists(constant.word_list_address):
        os.mkdir(constant.word_list_address)
        with open(constant.word_list_address, "w") as file:
            file.write("0")
        print("word list created")
        return
    else:
        with open(constant.word_list_address,"r") as file:
            word_list=file.read().split(",")       
    height=constant.word.winfo_height()
    width=constant.word.winfo_width()
    with open(constant.word_list_index,"r") as t1:
        constant.i=t1.read()
    if len(word_list) > 1:
        text = word_list[int(constant.i)]
    else:
        text = "No Word"

    # Calculate text size
    font_scale = 2.0
    thickness = 2
    font = cv.FONT_HERSHEY_COMPLEX
    (text_width, text_height), baseline = cv.getTextSize(text, font, font_scale, thickness)
    blank=np.zeros((height,width,3),dtype="uint8")
    x = (width - text_width) // 2
    y = (height + text_height) // 2  # because (0,0) is top-left in OpenCV
    # Put text
    cv.putText(blank, text, (x, y), font, font_scale, (0, 255, 255), thickness, cv.LINE_AA)
    img=Image.fromarray(blank)
    img=ImageTk.PhotoImage(img)
    constant.word.config(image=img)
    constant.word.image=img
    with open(constant.word_list_index,"w") as index:
        index.write(str((int(constant.i)+1)%len(word_list)))