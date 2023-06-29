import PySimpleGUI as sg
import engine
import FileOperations
import os
import sys

y_axis_options = ["gas volume", "umol", "TON", "PTON"]
gas_options = ["H2", "O2", "CO"]

# ----------------  Create Form  ---------------- #
layout = [
    [sg.Text('If you used the PhotocatGUI program, you do not need further data manipulation, just these parameters')],
    [sg.Text('Use cat for TON and PS for PTON. Put all datasets in a folder and choose this folder as input.')],
    [sg.Text('Select the folder with the excel files'), sg.Input(key='-IN-'), sg.FolderBrowse()],
    [sg.Text('What goes on the y-axis?'), sg.InputOptionMenu(y_axis_options, key='-Y-AXIS-')],
    [sg.Text('Which gas did you produce?'), sg.InputOptionMenu(gas_options, key='-GAS-PRODUCED-')],
    [sg.Text('Do you want to plot the fits?'), sg.InputOptionMenu(["y", "n"], key='-SHOW-FIT-')],
    [sg.Text('Do you want to adjust the y-axis limits? (y/n)?'), sg.InputOptionMenu(["y", "n"], key='-CHANGE-Y-LIMITS-')],
    [sg.Text('Maximum y-axis value (μL or μmol):'), sg.Input(key='-YMAX-')],
    [sg.Text('Minimum y-axis value (μL or μmol):'), sg.Input(key='-YMIN-')],
    [sg.Text('Font size of axis labels:'), sg.Slider(range=(1, 20), orientation='h', key='-LABEL-FONT-SIZE-'),
    sg.Text('Font size of tick labels:'), sg.Slider(range=(1, 20), orientation='h', key='-TICK-FONT-SIZE-')],
    [sg.Text('Font size of title:'), sg.Slider(range=(1, 20), orientation='h', key='-TITLE-FONT-SIZE-'),
    sg.Text('Font size of legend:'), sg.Slider(range=(1, 20), orientation='h', key='-LEGEND-FONT-SIZE-')],
    [sg.Text('Enter Title:'), sg.Input(key='-TITLE-')],
    [sg.Exit(), sg.Button("Calculate and Plot")]
    ]

# ----- Create the window ----- #
window = sg.Window("Photocatalysis stacker", layout)
window.finalize()

# try to update the window using the parameters from the parameters.json file in the current working directory
if os.path.exists("inparams.json"):
    parameters = FileOperations.read_file_as_parameters("inparams.json")
    window["-IN-"].update(parameters["-IN-"])
    window["-Y-AXIS-"].update(parameters["-Y-AXIS-"])
    window["-GAS-PRODUCED-"].update(parameters["-GAS-PRODUCED-"])
    window["-SHOW-FIT-"].update(parameters["-SHOW-FIT-"])
    window["-CHANGE-Y-LIMITS-"].update(parameters["-CHANGE-Y-LIMITS-"])
    window["-YMAX-"].update(parameters["-YMAX-"])
    window["-YMIN-"].update(parameters["-YMIN-"])
    window["-TITLE-"].update(parameters["-TITLE-"])
    window["-LABEL-FONT-SIZE-"].update(parameters["-LABEL-FONT-SIZE-"])
    window["-TICK-FONT-SIZE-"].update(parameters["-TICK-FONT-SIZE-"])
    window["-TITLE-FONT-SIZE-"].update(parameters["-TITLE-FONT-SIZE-"])
    window["-LEGEND-FONT-SIZE-"].update(parameters["-LEGEND-FONT-SIZE-"])

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WINDOW_CLOSED, "Exit"):
        sys.exit()
    if event == "Calculate and Plot":
        window.close()
        FileOperations.write_parameters_as_file("inparams.json", values)
        engine.execute(values)
        # write parameters to json in the input folder
