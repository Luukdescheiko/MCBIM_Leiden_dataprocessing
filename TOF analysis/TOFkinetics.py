import scienceplots
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from tkinter import filedialog
from tkinter import *

# set the plot style
plt.style.use(["science", "nature", "no-latex"])

# Dialog window to import the excel data sheet
root = Tk()
root.filename = filedialog.askopenfilename(initialdir="C:\\Users\\luuks\\OneDrive - Universiteit Leiden\\Stringer_Luuk", title="Select file",
                                             filetypes=(("Excel files", "*.xlsx"), ("all files", "*.*")))
root.destroy()

# Import the data sheet
data = pd.read_excel(filename)

# create new column with TOF per hour
time = data["Time (min)"]
TON = data["Fit TON(TDR)"]
# select only timepoints after 0
TON = TON[time >= 0]
time = time[time >= 0]
# take first derivative of TON
TOF = np.gradient(TON, time) * 60 # dTON/dt in h-1
# create new dataframe with time and TOF
data = pd.DataFrame()
data["Time (min)"] = time
data["TOF (h-1)"] = TOF

# create the plot from t = 0
plt.plot(time, TOF, color="black", linewidth=1)
plt.xlabel("Time (min)")
plt.ylabel("TOF (h$^{-1}$)")
plt.tight_layout()
# save dataset as csv to root
data.to_csv(os.path.join(filename[:-5] + "_TOF.csv"), index=False)
# save plot to root
plt.savefig(os.path.join(filename[:-5] + "_TOF.png"), dpi=300)

plt.show()
