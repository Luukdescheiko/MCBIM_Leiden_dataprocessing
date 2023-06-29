import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import json

reference_electrodes = ["$Fc^{+}/Fc$", "$Ag^{+}/AgCl$", "$NHE$", "$RHE$"]

# ----- Define GUI ----- #
layout = [[sg.Text('Select a file and output folder')],
            [sg.Input(key = 'PATH'), sg.FileBrowse()],
            [sg.Input(key='-OUTPUT-'), sg.FolderBrowse()],
            [sg.Text('Reference electrode')],
            [sg.InputOptionMenu(reference_electrodes, key='-REF-')],
            [sg.Text('Title')],
            [sg.InputText(key = 'TITLE')],
            [sg.Text('Save plot? (y/n)')],
            [sg.InputText(key = 'SAVE')],
            [sg.Text('Filename')],
            [sg.InputText(key='FILENAME')],
            [sg.Text('Correct potential with respect to Fc? (y/n)')],
            [sg.InputText(key='CORRECT')],
            [sg.Text('Correction factor')],
            [sg.InputText(key='CORRFAC')],
            [sg.Button('Submit'), sg.Button('Cancel')]]

import scienceplots
plt.style.use(['science', 'nature', 'no-latex'])

# --------------------------------- IMPORT VARIABLES --------------------------------- #
# create window
window = sg.Window('CV Plotter', layout)
window.Finalize()

# ----- update parameters from json file ----- #
if os.path.exists('CVparameters.json'):
    with open('CVparameters.json', 'r') as f:
        params = json.load(f)
        window['PATH'].update(params['PATH'])
        window['-OUTPUT-'].update(params['-OUTPUT-'])
        window['-REF-'].update(params['-REF-'])
        window['TITLE'].update(params['TITLE'])
        window['SAVE'].update(params['SAVE'])
        window['FILENAME'].update(params['FILENAME'])
        window['CORRECT'].update(params['CORRECT'])
        window['CORRFAC'].update(params['CORRFAC'])

# read values from window
event, values = window.read()

# define event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == 'Submit':
        # import parameters from window
        path = values['PATH']
        ref = values['-REF-']
        title = values['TITLE']
        save = values['SAVE']
        filename = values['FILENAME']
        correct = values['CORRECT']
        corrfac = float(values['CORRFAC'])
        # save values to json file
        with open('CVparameters.json', 'w') as f:

            json.dump(values, f)
        break
window.close()

print("The selected file is: " + path)

data = pd.read_csv(path)

# Set columns for potential and current
potcol = 0
curcol = 2

# make a dataframe with only the potential and current columns as float values
df = data.iloc[:, [potcol, curcol]]
df = df.astype(float)

# multiply current by 1000000 to get uA
df.iloc[:, 1] = df.iloc[:, 1] * 1000000

# ask if potential must be corrected for Fc
if correct == "y":
    # correct potential
    df.iloc[:, 0] = df.iloc[:, 0] - corrfac

# plot potential against current
plt.plot(df.iloc[:, 0], df.iloc[:, 1], linewidth=2)
plt.xlabel('E (V vs. ' + ref + ')')
plt.ylabel('i ('r'$\mu$A)')
plt.title(title)
if save == "y":
    # save to output folder
    plt.savefig(values['-OUTPUT-'] + "/" + filename + ".png", dpi=600)

plt.show()

# save plot data to csv in output folder
df.to_csv(values['-OUTPUT-'] + "/" + filename + ".csv", index=False)

print("DONE")
