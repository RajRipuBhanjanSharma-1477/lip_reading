from tkinter import *

root = Tk()
root.geometry("1000x700")

# Configure root window's grid
# root.grid_rowconfigure(0, weight=1)
# root.grid_rowconfigure(1, weight=2)
# root.grid_columnconfigure(0, weight=1)
# root.grid_columnconfigure(1, weight=1)

# Frame 1 - left side
t1f1 = LabelFrame(root, text="Frame 1", padx=10, pady=10, bg="lightgray")
t1f1.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)

# Frame 2 - top right
t1f2 = LabelFrame(root, text="Frame 2", padx=10, pady=10, bg="lightblue")
t1f2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Frame 3 - bottom right
t1f3 = LabelFrame(root, text="Frame 3", padx=10, pady=10, bg="lightpink")
t1f3.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

# Configure frames' internal grids (important!)
# for frame in [t1f1, t1f2, t1f3]:
#     frame.grid_rowconfigure(0, weight=1)
#     frame.grid_columnconfigure(0, weight=1)

# Add a label that fills inside each frame
Label(t1f1, text="This label fills Frame 1", bg="gray").grid(row=0, column=0, sticky="nsew")
Label(t1f2, text="This label fills Frame 2", bg="skyblue").grid(row=0, column=0, sticky="nsew")
Label(t1f3, text="This label fills Frame 3", bg="pink").grid(row=0, column=0, sticky="nsew")

root.mainloop()
