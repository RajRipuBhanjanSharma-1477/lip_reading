from tkinter import *
import cv2 as cv
from PIL import Image, ImageTk
import pygame
import pyaudio

# functional application
vid=None
camera_running=False
frame_width = 640
frame_height = 480
frame_ratio=0


def video():
    global live_feed,vid,frame_ratio
    istrue,frame=vid.read()
    if istrue:
        frame=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        if t1f1.winfo_width()>t1f1.winfo_height():
            new_frame_width=0.6*int(t1f1.winfo_width())
            new_frame_height=frame_ratio*new_frame_width
        else:
            new_frame_height=0.5*int(t1f1.winfo_height())
            new_frame_width=(1/frame_ratio)*new_frame_height
        frame=cv.resize(frame,(int(new_frame_width),int(new_frame_height)))
        img=Image.fromarray(frame)
        img=ImageTk.PhotoImage(img)
        live_feed.config(image=img)
        # live_feed.place_configure(
        #     x=int(camera_frame.winfo_width() / 2)-int(vid.get(cv.CAP_PROP_FRAME_WIDTH)/2),
        #     y=int(camera_frame.winfo_height() / 2)-int(vid.get(cv.CAP_PROP_FRAME_WIDTH)/2)
        # )
        live_feed.place_configure(
            x=int(camera_frame.winfo_width() / 2)-int(new_frame_width/2),
            y=int(camera_frame.winfo_height() / 2)-int(new_frame_height/2)
        )
        live_feed.image=img
        root.after(10,video)
    else:
        vid.release()
        return 0

def toggle():
    global camera_running,vid,frame_ratio
    if not camera_running:
        start.config(text="stop")
        camera_running=True
        vid=cv.VideoCapture(0)
        # Fetch frame dimensions from camera
        frame_ratio =int(vid.get(cv.CAP_PROP_FRAME_HEIGHT))/int(vid.get(cv.CAP_PROP_FRAME_WIDTH))
        video()
    else:
        start.config(text="start")
        camera_running=False
        live_feed.config(image="")
        vid.release()







# gui application 

root=Tk()
root.geometry("1000x700")
# Data collection tab_1

t1f1=LabelFrame(root,text="frame 1",width=500,height=700,padx=10,pady=10)
camera_frame=LabelFrame(t1f1,text="live Feed",bg="#006666",width=400,height=400,border=5)

t1f2=LabelFrame(root,text="frame 2",width=500,height=200,padx=10,pady=10)

t1f3=LabelFrame(root,text="frame 3",width=500,height=500,padx=10,pady=10)

# temporory label
# Label(t1f1,text="test").pack()
Label(t1f2,text="test").pack()
Label(t1f3,text="test").pack()

# adding live streaming window in tab1 frame 1

live_feed=Label(t1f1,text="Camera feed")
start=Button(t1f1,text="Start",command=toggle)



# tab 1 frame 1
t1f1.grid(row=0,column=0,rowspan=2,sticky="nsew",padx=4,pady=4)
camera_frame.grid(row=0,column=0,sticky="nsew",padx=2,pady=2)
live_feed.place(x=0,y=0)
start.grid(row=1,column=0)
# tab 1 frame 2
t1f2.grid(row=0,column=1,sticky="nsew",padx=4,pady=4)
# tab 2 frame 3
t1f3.grid(row=1,column=1,sticky="nsew",padx=4,pady=4)




root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)
t1f1.grid_rowconfigure(0, weight=4)
t1f1.grid_columnconfigure(0, weight=1)
t1f1.grid_rowconfigure(1,weight=1)
t1f2.grid_rowconfigure(0, weight=1)
t1f2.grid_columnconfigure(0, weight=1)
t1f3.grid_rowconfigure(1, weight=1)
t1f3.grid_columnconfigure(0, weight=1)\




root.mainloop()