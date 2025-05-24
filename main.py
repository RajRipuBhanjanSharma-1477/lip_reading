from tkinter import *
import component.constant as constant
from component import start
root=Tk()
root.title(constant.tittle)
root.geometry(constant.size)
start1=Button(root,text="start",command=lambda :start.START(root))
start1.grid(row=0,column=0)
root.bind("<KeyPress-r>",lambda event:constant.camera_stream_frame.start_recording())
root.bind("<KeyRelease-r>",lambda event:constant.camera_stream_frame.end_recording())
root.bind("<KeyPress-t>",lambda event:constant.video_stream_frame.toogle3())
root.bind("<KeyPress-s>",lambda event:constant.video_stream_frame.save_video())
root.mainloop()