import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
from PIL import Image, ImageTk
from record import Recorder as rec
from analyze import Analyzer as ana
import os

root = tk.Tk()
root.title("Aston Martin Cognizant F1AI")

author = tk.Label(root, text='Author: Charles Asselin\n'
                             'License: 111 267 783\n'
                             'Version 3.5.1', anchor='w', justify=tk.LEFT, bg='#F596C8', fg='black')
author.pack(fill='both')

canvas = tk.Canvas(root, height=700, width=700, bg="#006F62")
canvas.pack()

frame = tk.Frame(root, bg="#006F62")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

fontStyle = tkFont.Font(family="Lucida Grande", size=12)

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
solvers = ["Trendline Solver", "Basic Solver"]

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
    analyzer = ana(filename[0], variable.get())
    analyzer.analyze()
    label = tk.Label(frame, text=str(analyzer), bg="#006F62", fg='white', font=fontStyle)
    label.pack()

def change_dropdown(*args):
    print(variable.get())

variable = tk.StringVar(frame)
variable.set(solvers[0])
variable.trace('w', change_dropdown)

runSolver = tk.Button(frame, text="Run Solver", command=analyzecommand, highlightbackground="#006F62")
runSolver.pack(side=tk.BOTTOM)

w = tk.OptionMenu(frame, variable, *solvers)
w.config(bg="#006F62")
w.pack(side=tk.BOTTOM)
# chooselabel = tk.Label(frame, text="Choose a solver", fg='white', bg="#006F62")
# chooselabel.pack(side=tk.BOTTOM)

openFile = tk.Button(frame, text="Open File", command=openfile, highlightbackground="#006F62")
openFile.pack(side=tk.BOTTOM)

recordData = tk.Button(frame, text="Record Data", command=recordcommand, highlightbackground="#006F62")
recordData.pack(side=tk.TOP)

root.mainloop()
