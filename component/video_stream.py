from tkinter import *
import cv2 as cv
import component.constant as constant
from PIL import Image,ImageTk
import threading
import time
import pygame
from moviepy import VideoFileClip
import os
import shutil
from component import word
from tkinter import messagebox
import tkinter as tk
class video_container(LabelFrame):
    def __init__(self,parent):
        super().__init__(parent)
        constant.video_frame=LabelFrame(self,bg="#173cb2")
        constant.video_control_frame=LabelFrame(self,bg="#6a0891")
        constant.play=Button(constant.video_control_frame,text="Play",command=self.toogle3)
        constant.save=Button(constant.video_control_frame,text="Save",command=self.save_video)
        constant.delete=Button(constant.video_control_frame,text="Delete")
        constant.next=Button(constant.video_control_frame,text="next",command=word.display_word)
        constant.video=Label(constant.video_frame,text="hi",bg="#f29615")
        constant.video_frame.grid(row=0,column=0,sticky="nsew")
        constant.video_control_frame.grid(row=1,column=0,sticky="nsew")
        constant.video.place(x=0,y=0,relheight=1,relwidth=1)
        constant.play.grid(row=0,column=0)
        constant.save.grid(row=0,column=1)
        constant.delete.grid(row=0,column=2)
        constant.next.grid(row=0,column=3)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=5)
        self.grid_rowconfigure(1,weight=1)
    def start_video_playing(self):
        constant.playing=True
        constant.play.config(text="Stop")
        video_playing_thread=threading.Thread(target=self.video_play)
        video_playing_thread.start()
        audio_playing_thread = threading.Thread(target=self.audio_play)
        audio_playing_thread.start()

    def end_video_playing(self):
        if constant.capture:
                constant.playing=False
                constant.play.config(text="Play")
                constant.capture.release()
                constant.video_clip.close()
                constant.video_clip=None
                constant.capture=None

    def toogle3(self):
        if not constant.playing:
            self.start_video_playing()
            
        else:
            self.end_video_playing()
            
    def video_play(self):
        constant.capture=cv.VideoCapture("final_output.mp4")
        while constant.playing:
            a,b=constant.capture.read()
            if a:
                if not constant.playing:
                    break
                b=cv.cvtColor(b,cv.COLOR_BGR2RGB)
                c=Image.fromarray(b)
                width = constant.video_frame.winfo_width() or 500
                height = int(constant.frame_ratio*constant.video_frame.winfo_width()) or 500
                c = c.resize((width, height))
                c=ImageTk.PhotoImage(c)
                constant.video.config(image=c)
                constant.video.image=c
                time.sleep(1/30)
            else:
                constant.playing=False
                constant.play.config(text="Play")
                # constant.video.after(0, lambda: constant.play.config(text="Play"))
                constant.capture.release()
                constant.capture=None
                constant.video_clip.close()
                constant.video_clip=None
                break
    def audio_play(self):
        # Initialize pygame mixer
        pygame.mixer.init()

        # Load audio from the same video file
        constant.video_clip = VideoFileClip("final_output.mp4")
        audio_clip = constant.video_clip.audio
        audio_clip.write_audiofile("audio.wav", codec='pcm_s16le')

        # Play the extracted audio file
        constant.audio_player = pygame.mixer.Sound("audio.wav")
        constant.audio_player.play()

        # Wait for the audio to finish playing
        while constant.playing and pygame.mixer.get_busy():
            time.sleep(1/30)

        # Stop audio when done
        constant.audio_player.stop()
        constant.audio_player = None
    def save_video(self):
        print("save button is pressed")
        if not os.path.exists(constant.data_set_path):
            os.makedirs(constant.data_set_path)
            print(f"Directory created: {constant.data_set_path}")
        else:
            print(f"Directory already exists: {constant.data_set_path}")
        if not os.path.exists(constant.Only_Audio):
            os.makedirs(constant.Only_Audio)
            print(f"Directory created: {constant.Only_Audio}")
        else:
            print(f"Directory already exists: {constant.Only_Audio}")
        if not os.path.exists(constant.Only_Video):
            os.makedirs(constant.Only_Video)
            print(f"Directory created: {constant.Only_Video}")
        else:
            print(f"Directory already exists: {constant.Only_Video}")
        if not os.path.exists(constant.Video_Audio):
            os.makedirs(constant.Video_Audio)
            print(f"Directory created: {constant.Video_Audio}")
        else:
            print(f"Directory already exists: {constant.Video_Audio}")
        constant.data_set_count = self.load_data_set_count()
        constant.data_set_count=constant.data_set_count+1
        self.save_data_set_count(constant.data_set_count)
        shutil.copy2(constant.final_output,os.path.join(constant.Video_Audio,"video"+str(constant.data_set_count)+".mp4"))
        shutil.copy2(constant.video_recording,os.path.join(constant.Only_Video,"Only_video"+str(constant.data_set_count)+".avi"))
        shutil.copy2(constant.output_audio,os.path.join(constant.Only_Audio,"Only_video"+str(constant.data_set_count)+".wav"))
        self.show_notification("project","Recording Saved")
        word.display_word()

    def show_notification(self,title, message, duration=600):
        popup = tk.Toplevel()
        popup.title(title)
        popup.geometry("300x100")
        popup.resizable(False, False)
        popup.attributes("-topmost", True)

        label = tk.Label(popup, text=message, font=("Arial", 12))
        label.pack(expand=True, fill="both", padx=10, pady=10)

        # Auto-close after `duration` milliseconds
        popup.after(duration, popup.destroy)

    def load_data_set_count(self):
        if os.path.exists("data_set_count.txt"):
            with open("data_set_count.txt", "r") as file:
                count = int(file.read())
            print(f"Data set count loaded: {count}")
            return count
        else:
            print("No saved count found, starting from 0")
            return 0

    def save_data_set_count(self,count):
        with open("data_set_count.txt", "w") as file:
            file.write(str(count))
        print(f"Data set count saved: {count}")
    