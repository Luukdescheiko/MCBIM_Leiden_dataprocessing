import scienceplots
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
import tkinter as tk
import glob

plt.style.use(['science', 'nature', 'no-latex'])

# open file dialog to select file
root = tk.Tk()
root.withdraw()
filename = filedialog.askopenfilename(title="Select file")
root.destroy()

# read file
df = pd.read_excel(filename)

# plot CVs
ns = input("How many CVs do you want to plot? ")
ns = int(ns)
for i in range(ns):
    label = input("Label for CV " + str(i+1) + ": ")
    # plot column 1 + 4*i (potential) against column 2 + 4*i (current)
    plt.plot(df.iloc[:, 1+4*i], df.iloc[:, 2+4*i], label=label)
    plt.legend()
    plt.xlabel("Potential (V vs. Fc)")
    plt.ylabel("Current ($\mu$A)")


# save plot
save = input("Do you want to save the plot? (y/n) ")
if save == "y":
    # ask for filename
    filename = input("Filename: ")
    # save plot
    plt.savefig(filename + ".png", dpi=300, bbox_inches='tight')
    print("Plot saved as " + filename + ".png")

# show plot
plt.show()
