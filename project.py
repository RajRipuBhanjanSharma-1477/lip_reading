from tkinter import *
import cv2 as cv
from PIL import Image, ImageTk
import pygame
import pyaudio
import numpy as np
import wave
from moviepy import VideoFileClip, AudioFileClip

# functional application
vid=None
camera_running=False
recording=False
frame_width = 640
frame_height = 480
frame_ratio=0
p=None
stream=None
frame=None

def video():
    global live_feed,vid,frame_ratio,frame,recording
    istrue,frame=vid.read()
    if istrue:
        frame=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        if camera_frame.winfo_width()>camera_frame.winfo_height():
            new_frame_height=camera_frame.winfo_height()-20
            new_frame_width=(1/frame_ratio)*new_frame_height
        else:
            new_frame_width=camera_frame.winfo_width()-20
            new_frame_height=frame_ratio*new_frame_width

        frame=cv.resize(frame,(int(new_frame_width),int(new_frame_height)))
        if recording:
            cv.circle(frame,(15,20),10,(255,0,0),-1)
        img=Image.fromarray(frame)
        img=ImageTk.PhotoImage(img)
        live_feed.config(image=img)
        live_feed.place_configure(
            x=int((camera_frame.winfo_width() / 2)-int(new_frame_width/2)-10),
            y=int((camera_frame.winfo_height() / 2)-int(new_frame_height/2)-17)
        )
     
        live_feed.image=img
        root.after(10,video)
    else:
        vid.release()
        return 0
    



def audio_plot():
    global blank_image,stream
    if not camera_running:
        return 
    x1=0
    y1=blank_image.shape[0]//2
    x2=blank_image.shape[1]
    y2=blank_image.shape[0]//2
    cv.line(blank_image,(x1,y1),(x2,y2),(255,255,255),thickness=1)
    x1=blank_image.shape[1]//8
    y1=0
    x2=blank_image.shape[1]//8
    y2=blank_image.shape[1]
    cv.line(blank_image,(x1,y1),(x2,y2),(255,255,255),thickness=1)
    
    img=Image.fromarray(blank_image)
    img=ImageTk.PhotoImage(img)
    audio_graph.config(image=img)
    audio_graph.image=img
    audio_graph.place_configure(
        x=audio_frame.winfo_x(),
        y=audio_frame.winfo_y()
    )
    x1=blank_image.shape[1]//8
    y1=0
    x2=blank_image.shape[1]//8
    y2=blank_image.shape[1]
    cv.line(blank_image,(x1,y1),(x2,y2),(0,0,0),thickness=1)
    # graph plot
    data=np.frombuffer(stream.read(160,exception_on_overflow=False),dtype="int16")
    x1=blank_image.shape[1]//8
    y1=blank_image.shape[0]//2
    x2=blank_image.shape[1]//8
    # print(data)
    data=np.average(data)
    # print(data)
    data=data/32768
    # print(data)
    data=data*(blank_image.shape[0]//2)*100 # 1000 is the zoom
    # print(data)
    data=blank_image.shape[0]//2+data
    # print(data)
    y2=int(data)
    # print(y2)
    cv.line(blank_image,(x1,y1),(x2,y2),(255,255,255),thickness=1)


    # roatation
    blank_image = blank_image[:, :-1, :]
    new_column = np.zeros((blank_image.shape[0], 1, 3), dtype="uint8")
    blank_image = np.concatenate((new_column, blank_image), axis=1)

    root.after(10,audio_plot)



def toggle():
    global camera_running,vid,frame_ratio,blank_image,audio_graph,stream,p
    if not camera_running:
        start.config(text="stop")
        camera_running=True
        vid=cv.VideoCapture(0)
        # Fetch frame dimensions from camera
        frame_ratio =int(vid.get(cv.CAP_PROP_FRAME_HEIGHT))/int(vid.get(cv.CAP_PROP_FRAME_WIDTH))
        video()
        p=pyaudio.PyAudio()
        # audio graph
        stream=p.open(
            rate=16000,
            frames_per_buffer=1024,
            format=pyaudio.paInt16,
            channels=1,
            input=True
        )
        
        blank_image=np.zeros((audio_frame.winfo_height(),audio_frame.winfo_width(),3),dtype="uint8")
        audio_plot()
    else:
        start.config(text="start")
        camera_running=False
        live_feed.config(image="")
        audio_graph.config(image="")
        vid.release()
        stream.stop_stream()
        stream.close()
        p.terminate()
        p=None
frame_list=[]
audio_list=[]
def record():
    global frame,recording,live_feed,vid,frame_ratio,frame_list,audio_list
    if not recording:
        frame_list=[]
        audio_list=[]
        record_button.config(text="stop recording",bg="red")
        recording=True
        rec()
    else:
        recording=False
        record_button.config(text="recording",bg="green")
        if frame_list:
            height, width, _ = frame_list[0].shape
            out = cv.VideoWriter('output.avi', cv.VideoWriter_fourcc(*'XVID'), 30, (width, height))
            for f in frame_list:
                out.write(cv.cvtColor(f, cv.COLOR_RGB2BGR))  # RGB → BGR
            out.release()
            print("Video saved with", len(frame_list), "frames.")
        else:
            print("No frames recorded!")
        print(audio_list)
        if audio_list:
            wf = wave.open("output_audio.wav", 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(audio_list))
            wf.close()
            print("Audio saved. Total chunks:", len(audio_list))
        else:
            print("No audio recorded.")
        video = VideoFileClip("output.avi")
        audio = AudioFileClip("output_audio.wav")
        final = video.with_audio(audio)
        final.write_videofile("final_output.mp4", codec="libx264", audio_codec="aac")
def rec():
    global frame,vid,audio_list
    if recording:
        frame_list.append(frame.copy())
        audio_chunk = stream.read(1024)
        audio_list.append(audio_chunk)
    else:
        return
    root.after(10,rec)

    




# gui application 

root=Tk()
root.geometry("1000x700")
# Data collection tab_1


t1f1=LabelFrame(root,text="frame 1",pady=10)
camera_frame=LabelFrame(t1f1,text="live Feed",bg="#006666",border=5)
audio_frame=LabelFrame(t1f1,text="audio frame",bg="#445533")
t1f1_control_frame=LabelFrame(t1f1,text="control",bg="#778822")
t1f2=LabelFrame(root,text="frame 2")
t1f3=LabelFrame(root,text="frame 3")

# adding live streaming window in tab1 frame 1

live_feed=Label(camera_frame,text="Camera feed")
audio_graph=Label(root,text="audio graph",bg="#876746")
blank_image=np.zeros((10,10,3),dtype="uint8")
record_button=Button(t1f1_control_frame,text="Record",bg="green",command=record,height=1,width=12)
start=Button(t1f1_control_frame,text="Start",command=toggle)





# tab 1 frame 1
t1f1.grid(row=0,column=0,rowspan=2,sticky="nsew",padx=4,pady=4)
camera_frame.grid(row=0,column=0,sticky="nsew")
audio_frame.grid(row=1,column=0,sticky="nsew",padx=2,pady=2)
t1f1_control_frame.grid(row=2,column=0,sticky="nsew",padx=2,pady=2)

live_feed.grid(row=0,column=0)
# audio_graph.grid(row=0,column=0)
audio_graph.place()


start.grid(row=0,column=0)
record_button.grid(row=0,column=1)



# tab 1 frame 2
t1f2.grid(row=0,column=1,sticky="nsew",padx=4,pady=4)
# tab 2 frame 3
t1f3.grid(row=1,column=1,sticky="nsew",padx=4,pady=4)





root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
t1f1.grid_columnconfigure(0, weight=1)
t1f1.grid_rowconfigure(0, weight=6)
t1f1.grid_rowconfigure(1,weight=2)
t1f1.grid_rowconfigure(2,weight=1)
t1f2.grid_rowconfigure(0, weight=1)
t1f2.grid_columnconfigure(0, weight=1)
t1f3.grid_rowconfigure(1, weight=1)
t1f3.grid_columnconfigure(0, weight=1)




root.mainloop()