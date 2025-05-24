from tkinter import *
from PIL import Image,ImageTk
import component.constant as constant
import cv2 as cv
import threading
import pyaudio
import wave
from moviepy import VideoFileClip, AudioFileClip
import time
import os
from component.word import display_word
class Camera_stream_frame(LabelFrame):
    def __init__(self,parent):
        super().__init__(parent)
        constant.image_frame=LabelFrame(self)
        constant.control_frame=LabelFrame(self)
        constant.image_frame.grid(row=0,column=0,sticky="nsew")
        constant.control_frame.grid(row=1,column=0,sticky="nsew")
        constant.image=Image.open("./res/1.png")
        constant.image.thumbnail((500,500))
        constant.img=ImageTk.PhotoImage(constant.image)
        constant.video_stream=Label(constant.image_frame,image=constant.img)
        constant.video_stream.place(x=0,y=0)
        constant.start=Button(constant.control_frame,text="Start",command=self.toggle)
        constant.start.grid(row=0,column=0)
        constant.Record_Button=Button(constant.control_frame,text="record",command=self.toggle1)
        constant.Record_Button.grid(row=0,column=1)
        self.grid_rowconfigure(0,weight=5)
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)
    
    def toggle(self):
        if not constant.camera_running:
            video_thread=threading.Thread(target=self.video)
            video_thread.start()
            display_word()
        else:
            self.video_end()
            
    def video_end(self):
        constant.camera_running=False
        constant.start.config(text="start")
        constant.vid.release()

    def video(self):
        constant.camera_running=True
        constant.start.config(text="stop")
        constant.vid=cv.VideoCapture(0)
        constant.frame_ratio =int(constant.vid.get(cv.CAP_PROP_FRAME_HEIGHT))/int(constant.vid.get(cv.CAP_PROP_FRAME_WIDTH))
        while constant.camera_running:
            istrue,frame=constant.vid.read()
            if istrue:
                frame=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
                frame = cv.flip(frame, 1) 
                constant.cam_frame=frame
                constant.image=Image.fromarray(frame)
                width = constant.image_frame.winfo_width() or 500
                height = int(constant.frame_ratio*constant.image_frame.winfo_width()) or 500
                constant.image = constant.image.resize((width, height))
                constant.image=ImageTk.PhotoImage(constant.image)
                constant.video_stream.config(image=constant.image)
                constant.video_stream.image=constant.image
                # constant.stream.update_idletasks()
            else:
                return 0
            # cv.waitKey(2)
    def start_recording(self):
        if not constant.recording:
            constant.recording=True
            constant.Record_Button.config(text="recording")
            constant.p = pyaudio.PyAudio()
            constant.audio_stream=constant.p.open(
                rate=44100,
                frames_per_buffer=1024,
                format=pyaudio.paInt16,
                channels=1,
                input=True )
            constant.frame_record=[]
            constant.audio_record=[]
            # Delete previous recordings if they exist
            for file in [constant.video_recording,constant.output_audio,constant.final_output,"audio.wav"]:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"Deleted old file: {file}")
            constant.video_recording_thread=threading.Thread(target=self.frame_recording)
            constant.video_recording_thread.start()
            constant.audio_recording_thread=threading.Thread(target=self.audio_recording)
            constant.audio_recording_thread.start()

    def end_recording(self):
        constant.recording=False
        constant.video_recording_thread.join()
        constant.audio_recording_thread.join()
        constant.Record_Button.config(text="record")
        print(f"The number of frame recorded is {len(constant.frame_record)}")
        if constant.frame_record:
            height, width, _ = constant.frame_record[0].shape
            out = cv.VideoWriter(constant.video_recording, cv.VideoWriter_fourcc(*'XVID'), 30, (width, height))
            for f in constant.frame_record:
                out.write(cv.cvtColor(f, cv.COLOR_RGB2BGR))  # RGB → BGR
            out.release()
            print("Video saved with", len(constant.frame_record), "frames.")
        else:
            print("No frames recorded!")
        constant.frame_record=[]
        if constant.audio_record:
            wf = wave.open(constant.output_audio, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(constant.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(constant.audio_record))
            wf.close()
            print("Audio saved. Total chunks:", len(constant.audio_record))
        else:
            print("No audio recorded.")
        video = VideoFileClip(constant.video_recording)
        audio = AudioFileClip(constant.output_audio)
        final = video.with_audio(audio)
        final.write_videofile(constant.final_output, fps=30,codec="libx264", audio_codec="aac")
        constant.audio_stream.stop_stream()
        constant.audio_stream.close()
        audio.close()
        video.close()
        constant.p.terminate()
        constant.p=None
        constant.video_stream_frame.toogle3()


    def toggle1(self):
        if not constant.recording:
            self.start_recording()
        else:
            self.end_recording()
            
    def frame_recording(self):
        while constant.recording:
            constant.frame_record.append(constant.cam_frame)
            time.sleep(1/30) 
    def audio_recording(self):
            while constant.recording:
                audio_chunk = constant.audio_stream.read(1024)
                constant.audio_record.append(audio_chunk)
            
            
            
        
