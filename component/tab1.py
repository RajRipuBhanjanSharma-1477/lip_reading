from tkinter import *
from . import camera_stream,video_stream,word
import component.constant as constant
class Tab1(Frame):
    def __init__ (self,parent):
        super().__init__(parent)
        f1=LabelFrame(self,bg="#ec28bd")
        f1.grid(row=0,column=0,rowspan=2,sticky="nsew")
        f2=LabelFrame(self,bg="#a63e20")
        f2.grid(row=0,column=1,sticky="nsew")
        f3=LabelFrame(self,bg="#924acb")
        f3.grid(row=1,column=1,sticky="nsew")
       
        f1.grid_rowconfigure(0,weight=1)
        f1.grid_columnconfigure(0,weight=1)
        f3.grid_rowconfigure(0,weight=1)
        f3.grid_columnconfigure(0,weight=1)
        f2.grid_columnconfigure(0,weight=1)
        f2.grid_rowconfigure(0,weight=1)

        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=4)

        # print(f1.winfo_height(),f1.winfo_width())
        constant.f1_size=f1.winfo_width(),f1.winfo_height()
        constant.camera_stream_frame = camera_stream.Camera_stream_frame(f1)
        constant.camera_stream_frame.grid(row=0,column=0,sticky="nsew")
        constant.video_stream_frame=video_stream.video_container(f3)
        constant.video_stream_frame.grid(row=0,column=0,sticky="nsew")
        word_stream_frame=word.Word(f2)
        word_stream_frame.grid(row=0,column=0,sticky="nsew")
