from tkinter import *
from PIL import Image,ImageTk
flag=False
i=None
def put_image():
    global img,i
    i=Image.open(r"C:\Users\rajri\Desktop\Lipreading_project\lip_reading\res\1.png")
    i.thumbnail((400,400))
    i=ImageTk.PhotoImage(i)
    img.config(image=i)
    img.image=i
def toggle():
    global flag,i
    if not flag:
        put_image()
        flag=True
    else:
        img.config(image="")
        img.image=""
        flag=False
        i=None
def release_image():
    global flag,i,img
    img.config(image="")
    img.image=""
    flag=False
    i=None
root=Tk()
root.geometry("500x500")
root.title("The key binding exprement")
image_frame=LabelFrame(root)
img=Label(image_frame)
button=Button(root,text="image",command=toggle)
image_frame.grid(row=0,column=0,sticky="nsew")
button.grid(row=1,column=0,sticky="nsew")
img.place(x=0,y=0,relheight=1,relwidth=1)
root.grid_rowconfigure(0,weight=5)
root.grid_rowconfigure(1,weight=1)
root.grid_columnconfigure(0,weight=1)
root.bind("<KeyPress-space>",lambda event:put_image())
root.bind("<KeyRelease-space>",lambda event:release_image())
root.mainloop()


