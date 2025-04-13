from tkinter import *
from PIL import Image,ImageTk
import cv2 as cv
import numpy as np
import pyaudio as pa
import wave
x1,x2,y1,y2=0,0,0,0
blank_image=np.zeros((500,500,3),dtype="uint8")
p=pa.PyAudio()
stream=p.open(
    rate=32000,
    frames_per_buffer=320,
    format=pa.paInt16,
    channels=1,
    input=True
)
def audio_plot():
    global x1,x2,y1,y2,blank_image
    # blank_image=np.zeros((win.winfo_height(),win.winfo_width(),3),dtype="uint8")
    x1=0
    y1=blank_image.shape[0]//2
    x2=blank_image.shape[1]
    y2=blank_image.shape[0]//2
    cv.line(blank_image,(x1,y1),(x2,y2),(255,255,255),thickness=1)
    x1=blank_image.shape[1]//8
    y1=0
    x2=blank_image.shape[1]//8
    y2=blank_image.shape[0]
    cv.line(blank_image,(x1,y1),(x2,y2),(255,255,255),thickness=1)
    data=np.frombuffer(stream.read(320,exception_on_overflow=False),dtype="int16")
    print(data)
    # data=int((data/(2**15))*blank_image.shape[0])
    # data = int((data / 32768.0) * (blank_image.shape[0] // 2))
    # x1=blank_image.shape[1]//8
    # y1=blank_image.shape[0]//2
    # x2=blank_image.shape[1]//8
    # y2=int(blank_image.shape[0]//2+data)
    # print(y2)
    # cv.line(blank_image,(x1,y1),(x2,y2),(255,255,255),thickness=1)
    img=Image.fromarray(blank_image)
    img=ImageTk.PhotoImage(img)
    plot.config(image=img)
    plot.image=img
    plot.place_configure(
        x=0,
        y=0

    )
    x1=blank_image.shape[1]//8
    y1=0
    x2=blank_image.shape[1]//8
    y2=blank_image.shape[0]
    cv.line(blank_image,(x1,y1),(x2,y2),(0,0,0),thickness=1)



    x1=blank_image.shape[1]//8
    y1=blank_image.shape[0]//2
    x2=blank_image.shape[1]//8
    data=np.average(data)
    print(data)
    data=data/32768
    print(data)
    data=data*(blank_image.shape[0]//2)*10000 # 1000 is the zoom
    print(data)
    data=blank_image.shape[0]//2+data
    print(data)
    y2=int(data)
    print(y2)
    cv.line(blank_image,(x1,y1),(x2,y2),(255,255,255),thickness=1)
    

    
    blank_image = blank_image[:, :-1, :]
    new_column = np.zeros((blank_image.shape[0], 1, 3), dtype="uint8")
    blank_image = np.concatenate((new_column, blank_image), axis=1)
    root.after(10,audio_plot)




root=Tk()
root.geometry("500x500")
win=LabelFrame(root,text="Audio Signal",bg="green")
control=LabelFrame(root,text="control",bg="pink")
plot=Label(win,text="audio plot label")
button=Button(control,text="Start",command=audio_plot)
# creating a blank image and putin in the plot label




win.grid(row=0,column=0,sticky="nsew")
control.grid(row=1,column=0,sticky="nsew")
plot.grid(row=0,column=0)
button.grid(row=0,column=0)


root.grid_columnconfigure(0,weight=1)
root.grid_rowconfigure(0,weight=6)
root.grid_rowconfigure(1,weight=1)

win.grid_rowconfigure(0,weight=1)
win.grid_columnconfigure(0,weight=1)

control.grid_rowconfigure(0,weight=1)
control.grid_columnconfigure(0,weight=1)


# plot.grid_rowconfigure(0,weight=1)
# plot.grid_columnconfigure(0,weight=1)








root.mainloop()