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



def video():
    global live_feed,vid,frame_width, frame_height
    istrue,frame=vid.read()
    if istrue:
        frame=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        # Get current label dimensions
        label_w = live_feed.winfo_width()
        label_h = live_feed.winfo_height()

        if label_w > 0 and label_h > 0:
            # Determine target width and height maintaining aspect ratio
            label_aspect = label_w / label_h
            frame_aspect = frame_width / frame_height

            if frame_aspect > label_aspect:
                # Frame is wider than label, fit to width
                new_w = label_w
                new_h = int(label_w / frame_aspect)
            else:
                # Frame is taller than label, fit to height
                new_h = label_h
                new_w = int(label_h * frame_aspect)

            frame = cv.resize(frame, (new_w, new_h))

         # Create a new image with label size and paste resized frame into center
        final_img = Image.new("RGB", (label_w, label_h), color=(0, 102, 102))  # match your bg color #006666
        img_pil = Image.fromarray(frame)
        final_img.paste(img_pil, ((label_w - new_w) // 2, (label_h - new_h) // 2))

        # img=Image.fromarray(final_img)
        img=ImageTk.PhotoImage(final_img)
        live_feed.config(image=img)
        live_feed.image=img
        root.after(10,video)
    else:
        vid.release()
        return 0

def toggle():
    global camera_running,vid,frame_width, frame_height
    if not camera_running:
        start.config(text="stop")
        camera_running=True
        vid=cv.VideoCapture(0)

        # Fetch frame dimensions from camera
        frame_width = int(vid.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_height = int(vid.get(cv.CAP_PROP_FRAME_HEIGHT))

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

live_feed=Label(camera_frame,text="Camera feed")
start=Button(t1f1,text="Start",command=toggle)



# tab 1 frame 1
t1f1.grid(row=0,column=0,rowspan=2,sticky="nsew",padx=4,pady=4)
camera_frame.grid(row=0,column=0,sticky="nsew",padx=2,pady=2)
live_feed.pack(fill=BOTH,expand=True)
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
t1f3.grid_columnconfigure(0, weight=1)
root.mainloop()