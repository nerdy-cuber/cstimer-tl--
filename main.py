import matplotlib.pyplot as plt
import tkinter as tk
from ast import literal_eval
from tkinter import filedialog
from datetime import datetime as dt
import json


# Get data from file
cstimerfile = filedialog.askopenfilename(title="Please choose a .txt or .json file to open:")  # opens file


with open(cstimerfile) as f:
    file = json.loads(f.read())
    sessions = list(file.values())
    sessions.pop()
    properties = file["properties"]["sessionData"]  # extracts properties value from file, which contains all the names and ranks
    properties = properties.replace("\\", "")  # reformats string
    properties = properties.replace("null", "None")  # reformats string
    properties = literal_eval(properties)  # converts string to dict
    names = [item["name"] for item in properties.values()]  # extracts names
    ranks = [item["rank"] for item in properties.values()]  # extracts ranks
    names = [name for _, name in sorted(zip(ranks, names))]  # list of ranked names
    sessions = [session for _, session in sorted(zip(ranks, sessions))]  # list of ranked sessions

# Select the session
master = tk.Tk()
master.title("Please choose a session:")
m = tk.StringVar()
master.geometry("300x100")
menu_default = "Choose one"

def main():  # Get name choice
    while True:
        session = sessions[names.index(m.get())]  # Finds corresponding session with name
        submit_button.config(state="disabled")
        plot(session)
        submit_button.config(state="normal")
        m.set(menu_default)  # resets after plot is closed


def plot(session):
    times = [sum(solve[0])/1000 for solve in session]  # extracts times
    timestamps = [dt.fromtimestamp(solve[3]) for solve in session]  # extracts timestamps
    plt.scatter(timestamps, times)
    plt.show()


menu = tk.OptionMenu(master, m, menu_default, *names)
menu.pack()
submit_button = tk.Button(master, text="Submit", command=main)
submit_button.pack()
tk.mainloop()