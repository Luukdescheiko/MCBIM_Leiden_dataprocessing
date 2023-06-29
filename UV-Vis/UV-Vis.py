# import required packages
import os
import json
import numpy as np
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from scipy import signal
import scienceplots
plt.style.use(['science', 'nature', 'no-latex'])

# --------------------------------- GUI --------------------------------- #
# define layout for entering parameters
layout = [
    [sg.Text("Please select the file:"), sg.Input(key="-IN-"), sg.FileBrowse(file_types=(("csv Files", "*.csv"),))],
    [sg.Text("Please enter the output folder:"), sg.Input(key="-OUT-"), sg.FolderBrowse()],
    [sg.Text("Please enter the number of samples:")],
    [sg.InputText(key="-NS-")],
    [sg.Text("Please enter the number of repetitions:")],
    [sg.InputText(key="-REPS-")],
    [sg.Text("Please enter the minimum wavelength (nm):")],
    [sg.InputText(key="-MINWL-")],
    [sg.Text("Please enter the maximum wavelength (nm):")],
    [sg.InputText(key="-MAXWL-")],
    [sg.Text("Please enter the measurement resolution (nm):")],
    [sg.InputText(key="-RES-")],
    [sg.Text("Please enter the number of the first column:")],
    [sg.InputText(key="-STARTCOL-")],
    [sg.Text("Please enter the names of the samples separated by commas:")],
    [sg.InputText(key="-SAMPLENAMES-")],
    [sg.Text("Please enter the minimum wavelength for the zoomed in plot (nm):")],
    [sg.InputText(key="-MINWLZOOM-")],
    [sg.Text("Please enter the maximum wavelength for the zoomed in plot (nm):")],
    [sg.InputText(key="-MAXWLZOOM-")],
    [sg.Text("Please enter the maximum absorbance for the zoomed in plot:")],
    [sg.InputText(key="-MAXABSZOOM-")],
    [sg.Text("Please enter the title:")],
    [sg.InputText(key="-TITLE-")],
    [sg.Text("Please enter the output file name:")],
    [sg.InputText(key="-FILENAME-")],
    [sg.Button("Ok")]
    ]

# create window
window = sg.Window("File Browser", layout)

sg.Window.finalize(window)

# ----- update parameters from json file ----- #
if os.path.exists('UVparameters.json'):
    with open('UVparameters.json', 'r') as f:
        params = json.load(f)
        window["-IN-"].update(params["-IN-"])
        window["-OUT-"].update(params["-OUT-"])
        window["-NS-"].update(params["-NS-"])
        window["-REPS-"].update(params["-REPS-"])
        window["-MINWL-"].update(params["-MINWL-"])
        window["-MAXWL-"].update(params["-MAXWL-"])
        window["-RES-"].update(params["-RES-"])
        window["-STARTCOL-"].update(params["-STARTCOL-"])
        window["-SAMPLENAMES-"].update(params["-SAMPLENAMES-"])
        window["-MINWLZOOM-"].update(params["-MINWLZOOM-"])
        window["-MAXWLZOOM-"].update(params["-MAXWLZOOM-"])
        window["-MAXABSZOOM-"].update(params["-MAXABSZOOM-"])
        window["-TITLE-"].update(params["-TITLE-"])
        window["-FILENAME-"].update(params["-FILENAME-"])


# define event loop
while True:
    event, values = window.read()
    if event == "Ok":
        # import parameters from GUI
        path = values["-IN-"]
        outpath = values["-OUT-"]
        ns = int(values["-NS-"])
        reps = int(values["-REPS-"])
        minwl = int(values["-MINWL-"])
        maxwl = int(values["-MAXWL-"])
        resolution = int(values["-RES-"])
        startcolumn = int(values["-STARTCOL-"])
        sample_names = values["-SAMPLENAMES-"].split(",")
        minwlzoom = int(values["-MINWLZOOM-"])
        maxwlzoom = int(values["-MAXWLZOOM-"])
        maxabszoom = int(values["-MAXABSZOOM-"])
        filename = values["-FILENAME-"]
        title = values["-TITLE-"]
        # save parameters as json file
        with open('UVparameters.json', 'w') as f:
            json.dump(values, f)
        break
    if event == "Select file":
        root = tk.Tk()
        root.withdraw()
        path = os.path.abspath(filedialog.askopenfilename(
            initialdir=".\\data"))
        print("The selected file is: " + path)
    if event == "Select folder":
        root = tk.Tk()
        root.withdraw()
        path = os.path.abspath(filedialog.askdirectory(
            initialdir=".\\data"))
        print("The selected folder is: " + path)

print(sample_names)

# close window
window.close()

# --------------------------------- CODE --------------------------------- #

# state requirements
print("Please note that this code works only when absorption columns are separated an equal mount of places from each \
other (single/diplo/triplo measurements).  If this is not the case, please change the code accordingly. You can tell \
the code where to start counting. NOTE: the first column is number 0.")

# n, needed for dataframe slicing, DO NOT CHANGE
n = int(2 + (maxwl - minwl) / resolution)

# import csv file
data = pd.read_csv(path)

# # make plot
# fig = go.Figure()
# for i in range(ns):
#     for j in range(reps):
#         df = data.iloc[1:n:1]
#         Wavelength = np.array(df.iloc[:, 0], dtype=float)
#         Absorbance = np.array(df.iloc[:, int(startcolumn + i * reps + j)], dtype=float)
#         fig.add_trace(go.Scatter(x=Wavelength, y=Absorbance, mode='lines', name=(sample_names[i] + " " + str(j + 1))))


# create new dataframes with only wavelengths and absorbance of all samples
df = data.iloc[1:n:1]
# make wavelength array starting from minwl to maxwl with resolution nm
Wavelength = np.array(df.iloc[:, 0], dtype=float)
# create array for absorbance
Absorbances = np.zeros((ns, reps, len(Wavelength)))
for i in range(ns):
    Absorbance = np.array(df.iloc[:, int(startcolumn+reps*i*2)], dtype=float)
    # append absorbance to array
    Absorbances[i, 0, :] = Absorbance
    plt.plot(Wavelength, Absorbance, label=(sample_names[i]))
plt.xlabel('Wavelength (nm)')
plt.ylabel('Absorbance')
plt.title(title)
# ask if legend is needed
plt.legend(labels=sample_names, loc='upper right')

# ask if plot needs to be zoomed in
plt.xlim(minwlzoom, maxwlzoom)
plt.ylim(0, maxabszoom)

# make new df from Wavelengths and Absorbances
df = pd.DataFrame(Wavelength, columns=["Wavelength"])
for i in range(ns):
    df[sample_names[i]] = Absorbances[i, 0, :]

# Ask if user wants to save the plot
plt.savefig(os.path.join(outpath, filename + ".png"), dpi=600)
# save data as filename_data + .csv to outpath
df.to_csv(os.path.join(outpath, filename + "_data.csv"), index=False)
# save UV parameters as filename_UVparameters + .json to outpath
with open(os.path.join(outpath, filename + "_UVparameters.json"), 'w') as f:
    json.dump(values, f)


plt.show()

# # Ask if user wants to calculate extinction coefficient
# extinction = input("Do you want to calculate the extinction coefficient? (y/n): ")
# if extinction == "y":
#     # switch the dataset upside down
#     extdata = df.iloc[::-1]
#     # reverse index
#     extdata.index = range(len(extdata.index))
#     Wavelength = np.array(extdata.iloc[:, 0], dtype=float)
#     Eabs = []
#     # ask for boundary wavelengths
#     lowerbound = int(input("Enter the lower bound of the wavelength range for the maximum (nm): "))
#     lb = int((lowerbound - minwl) / resolution)
#     upperbound = int(input("Enter the upper bound of the wavelength range for the maximum (nm): "))
#     ub = int((upperbound - minwl) / resolution)
#     # ask pathlength of cuvette
#     pathlength = float(input("Enter the pathlength of the cuvette (cm): "))
#     molarities = []
#     # find maximum absorbance and corresponding wavelength
#     maxabs = []
#     maxabswl = []
#     molarities = UVP.molarities
#     for i in range(ns):
#         Absorbance = np.array(extdata.iloc[:, int(startcolumn + 2 * reps * i)], dtype=float)
#         maxabs.append(max(Absorbance[lb:ub]))
#         maxabswl.append(Wavelength[np.argmax(Absorbance[lb:ub])])
#         print("The maximum absorbance of sample %s is: %f" % (sample_names[i], maxabs[i]), " at a wavelength of %f nm" % (maxabswl[i]))
#         # create list of molarities
#         # calculate extinction coefficient
#         E = maxabs[i] / (molarities[i] * pathlength)
#         Eabs.append(E)
#         print("The extinction coefficient of sample %d is: %f M-1 cm-1" % (i+1, E))
#     print(Eabs)
# else: print("Extinction coefficient not calculated")
#
# # add remark in plot# show plot
# # plt.show()
# #
# # plt.text(lambdamax, Eabs[0], $λ_{max}$, transform=plt.gcf().transFigure)
#
