from tkinter import *
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np

# Initialize window
root = Tk()
root.geometry("500x550")
root.title("Tic Tac Toe")

turn = True  # True = X, False = O
board = [""] * 9

# Label for current player
playerLabel = Label(root, text="Player X's Turn", font=('Helvetica', 16))
playerLabel.grid(row=0, column=0)

# Create blank board image with grid lines
blankImage = np.zeros((500, 500, 3), dtype="uint8")
cv.line(blankImage, (166, 0), (166, 500), (255, 255, 255), thickness=3)
cv.line(blankImage, (332, 0), (332, 500), (255, 255, 255), thickness=3)
cv.line(blankImage, (0, 166), (500, 166), (255, 255, 255), thickness=3)
cv.line(blankImage, (0, 332), (500, 332), (255, 255, 255), thickness=3)

img1 = Image.fromarray(blankImage)
img1 = ImageTk.PhotoImage(img1)

# Image label
bimage = Label(root, image=img1)
bimage.grid(row=1, column=0)

# Button action function
def but(index):
    global turn
    if board[index] == "":
        board[index] = "X" if turn else "O"
        buttons[index].config(text=board[index], state=DISABLED)
        if check_winner():
            playerLabel.config(text=f"Player {'X' if turn else 'O'} Wins!")
            for b in buttons:
                b.config(state=DISABLED)
        elif "" not in board:
            playerLabel.config(text="It's a Draw!")
        else:
            turn = not turn
            playerLabel.config(text=f"Player {'X' if turn else 'O'}'s Turn")

def check_winner():
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for cond in win_conditions:
        if board[cond[0]] == board[cond[1]] == board[cond[2]] != "":
            return True
    return False

# Create and place buttons
buttons = []
positions = [
    (41, 41), (207, 41), (373, 41),
    (41, 207), (207, 207), (373, 207),
    (41, 373), (207, 373), (373, 373)
]
for i in range(9):
    b = Button(bimage, text="", height=6, width=12, padx=1, pady=1,
               command=lambda i=i: but(i))
    b.place(x=positions[i][0], y=positions[i][1])
    buttons.append(b)

root.mainloop()
