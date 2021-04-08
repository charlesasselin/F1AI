import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from record import Recorder as rec
from analyze import Analyzer as ana
import os

root = tk.Tk()
root.title("Aston Martin Cognizant F1AI")
canvas = tk.Canvas(root, height=700, width=700, bg="#006F62")
canvas.pack()

frame = tk.Frame(root, bg="#006F62")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)


basewidth = 300
logo = Image.open('images/amf1logo.png')
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo.convert("RGB"))
logolabel = tk.Label(frame, image=logo)
logolabel.image = logo
logolabel.pack(side=tk.TOP)

filename = []
def openfile():
    file = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File',)
    print(file)
    filename.append(os.path.split(file)[1])
    print(filename)

def recordcommand():
    rec().record()

def analyzecommand():
    handle = filename[0]
    print(handle)
    if len(filename) == 0:
        raise ValueError('No data files have been selected')
    ana(filename[0], 'basic').analyze()


runSolver = tk.Button(frame, text="Run Solver", command=analyzecommand, highlightbackground="#006F62")
runSolver.pack(side=tk.BOTTOM)

openFile = tk.Button(frame, text="Open File", command=openfile, highlightbackground="#006F62")
openFile.pack(side=tk.BOTTOM)

recordData = tk.Button(frame, text="Record Data", command=recordcommand, highlightbackground="#006F62")
recordData.pack(side=tk.BOTTOM)

root.mainloop()
