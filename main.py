import re
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
from ast import literal_eval
from tkinter import filedialog
from datetime import datetime as dt


# Get data from file
cstimerfile = filedialog.askopenfilename(title="Please choose a .txt file to open:")  # opens file

re_sessions = re.compile(r'session\d+":(\[]|.+?]])')
re_names = re.compile(r'name\\":\\"(.+?)\\')
re_ranks = re.compile(r'rank\\":(\d+)')
with open(cstimerfile) as f:
    file = f.read()
    ranks = re_ranks.findall(file)
    ranks = [int(rank) for rank in ranks]  # convert ranks from str to int
    names = re_names.findall(file)  # list of names
    sessions = re_sessions.findall(file)  # list of sessions
    sessions = [np.array([session, name]) for session, name in zip(sessions, names)]  # list of arrays of sessions + name
    sessions = np.array([session for _, session in sorted(zip(ranks, sessions))])  # array of ranked sessions


# Select the session
master = tk.Tk()
master.title("Please choose a session:")
m = tk.StringVar()
master.geometry("300x100")


def get_input():  # Get session choice
    global session
    session = sessions[np.where(sessions==m.get())[0]]  # find corresponding session of name
    session = session.reshape(2)
    session = session[0]
    master.destroy()


menu = tk.OptionMenu(master, m, *sessions[:, 1])  # get column 2 of sessions list
menu.pack()
submit_button = tk.Button(master, text="Submit", command=get_input)
submit_button.pack()
tk.mainloop()