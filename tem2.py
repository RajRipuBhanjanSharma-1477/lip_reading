from tkinter import *
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
import pyaudio as pa

# Create initial blank image
height, width = 500, 500
blank_image = np.zeros((height, width, 3), dtype="uint8")

# Draw initial horizontal center line (once)
cv.line(blank_image, (0, height // 2), (width, height // 2), (255, 255, 255), thickness=1)

# Setup audio stream
p = pa.PyAudio()
stream = p.open(
    rate=16000,  # more realistic sample rate
    frames_per_buffer=1024,
    format=pa.paInt16,
    channels=1,
    input=True
)

# GUI setup
root = Tk()
root.geometry("500x500")

win = LabelFrame(root, text="Audio Signal", bg="green")
control = LabelFrame(root, text="Control", bg="pink")
plot = Label(win)
button = Button(control, text="Start", command=lambda: audio_plot())

win.grid(row=0, column=0, sticky="nsew")
control.grid(row=1, column=0, sticky="nsew")
plot.grid(row=0, column=0)
button.grid(row=0, column=0)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=6)
root.grid_rowconfigure(1, weight=1)

win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(0, weight=1)
control.grid_rowconfigure(0, weight=1)
control.grid_columnconfigure(0, weight=1)

# Audio plot function
def audio_plot():
    global blank_image

    # Read audio buffer
    data = np.frombuffer(stream.read(1024, exception_on_overflow=False), dtype="int16")
    value = int(np.average(np.abs(data)))  # Use absolute average for better results

    # Scale value to image height
    amplitude = int((value / 32768.0) * (height // 2))
    amplitude = np.clip(amplitude, 0, height // 2)

    # Scroll image left by 1 pixel
    blank_image = np.roll(blank_image, -1, axis=1)
    blank_image[:, -1] = 0  # Clear the rightmost column

    # Draw new line on right edge
    center_y = height // 2
    cv.line(blank_image,
            (width - 1, center_y - amplitude),
            (width - 1, center_y + amplitude),
            (0, 255, 0), thickness=1)

    # Redraw center line (optional, if it fades away)
    blank_image[center_y:center_y + 1, -1] = (255, 255, 255)

    # Update GUI
    img = Image.fromarray(blank_image)
    img = ImageTk.PhotoImage(img)
    plot.config(image=img)
    plot.image = img

    # Repeat after 30 ms
    root.after(30, audio_plot)

root.mainloop()
