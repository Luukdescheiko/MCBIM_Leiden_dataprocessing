import PySimpleGUI as sg
import json
import engine
import os
import sys

y_n = ["y", "n"]

# ----- Define GUI ----- #
# define layout for entering parameters
layout = [
    [sg.Text("Please select the file:"), sg.Input(key="-IN-"), sg.FileBrowse(file_types=(("csv Files", "*.csv"),))],
    [sg.Text("Please enter the output folder:"), sg.Input(key="-OUT-"), sg.FolderBrowse()],
    [sg.Text("Please enter the end time of irradiation:"),
    sg.InputText(key="-TFINAL-")],
    [sg.Text("Please enter the length of the cycle:"),
    sg.InputText(key="-TCYCLE-")],
    [sg.Text("Please enter the minimum wavelength (nm):"),
    sg.InputText(key="-MINWL-")],
    [sg.Text("Please enter the maximum wavelength (nm):"),
    sg.InputText(key="-MAXWL-")],
    [sg.Text("Please enter the measurement resolution (nm):"),
    sg.InputText(key="-RES-")],
    [sg.Text("Please enter the minimum wavelength of zoomed plot (nm):"),
    sg.InputText(key="-MINWLZOOM-")],
    [sg.Text("Please enter the maximum wavelength of zoomed plot (nm):"),
    sg.InputText(key="-MAXWLZOOM-")],
    [sg.Text("Please enter the maximum absorbance of zoomed plot:"),
    sg.InputText(key="-MAXABSZOOM-")],
    [sg.Text("Do you want a time-resolved inset?"),
    sg.InputOptionMenu(y_n, key="-INSET-")],
    [sg.Text("Please enter the wavelengths for time-resolved inset separated by commas:"),
    sg.InputText(key="-INSETWL-")],
    [sg.Text("Please enter the title:"),
    sg.InputText(key="-TITLE-")],
    [sg.Text("Do you want to put an absorbance spectrum on top of the plot?"),
    sg.InputOptionMenu(y_n, key="-ABS-SPEC-OVERLAY-")],
    [sg.Text("Do you want to multiply the abs spectrum?"),
    sg.InputOptionMenu(y_n, key="-MULTIPLY-")],
    [sg.Text("If yes, please enter multiplication factor:"),
    sg.InputText(key="-MULTIPLY-FACTOR-")],
    [sg.Text("Do you want to add a dark control to the inset plot?"),
    sg.InputOptionMenu(y_n, key="-DARK-CONTROL-")],
    [sg.Text("Dark control wavelengths"),
    sg.InputText(key="-DARK-CONTROL-WLS-")],
    [sg.Text("Please enter the output file name:"),
    sg.InputText(key="-FILENAME-")],
    [sg.Text('Font size of axis labels:'), sg.Slider(range=(1, 20), orientation='h', key='-LABEL-FONT-SIZE-'),
    sg.Text('Font size of tick labels:'), sg.Slider(range=(1, 20), orientation='h', key='-TICK-FONT-SIZE-')],
    [sg.Text('Font size of title:'), sg.Slider(range=(1, 20), orientation='h', key='-TITLE-FONT-SIZE-'),
    sg.Text('Font size of legend:'), sg.Slider(range=(1, 20), orientation='h', key='-LEGEND-FONT-SIZE-')],
    [sg.Button("OK"), sg.Button("Import values from json file")]
 ]

# ----- Create GUI ----- #
window = sg.Window("Irradiation photostability", layout)
sg.Window.finalize(window)

# import values from json file if it exists
if os.path.exists('PhotStab_input.json'):
    with open('PhotStab_input.json', 'r') as f:
        values = json.load(f)
        window["-IN-"].update(values["-IN-"])
        window["-OUT-"].update(values["-OUT-"])
        window["-TFINAL-"].update(values["-TFINAL-"])
        window["-TCYCLE-"].update(values["-TCYCLE-"])
        window["-MINWL-"].update(values["-MINWL-"])
        window["-MAXWL-"].update(values["-MAXWL-"])
        window["-RES-"].update(values["-RES-"])
        window["-TITLE-"].update(values["-TITLE-"])
        window["-FILENAME-"].update(values["-FILENAME-"])
        window["-MINWLZOOM-"].update(values["-MINWLZOOM-"])
        window["-MAXWLZOOM-"].update(values["-MAXWLZOOM-"])
        window["-MAXABSZOOM-"].update(values["-MAXABSZOOM-"])
        window["-INSET-"].update(values["-INSET-"])
        window["-INSETWL-"].update(values["-INSETWL-"])
        window["-LABEL-FONT-SIZE-"].update(values["-LABEL-FONT-SIZE-"])
        window["-TICK-FONT-SIZE-"].update(values["-TICK-FONT-SIZE-"])
        window["-TITLE-FONT-SIZE-"].update(values["-TITLE-FONT-SIZE-"])
        window["-LEGEND-FONT-SIZE-"].update(values["-LEGEND-FONT-SIZE-"])
        try:
            window["-ABS-SPEC-OVERLAY-"].update(values["-ABS-SPEC-OVERLAY-"])
            window["-DARK-CONTROL-"].update(values["-DARK-CONTROL-"])
            window["-MULTIPLY-"].update(values["-MULTIPLY-"])
            window["-MULTIPLY-FACTOR-"].update(values["-MULTIPLY-FACTOR-"])
            window["-DARK-CONTROL-"].update(values["-DARK-CONTROL-"])
            window["-DARK-CONTROL-WLS-"].update(values["-DARK-CONTROL-WLS-"])
        except:
            pass
# ----- Event Loop ----- #
while True:
    event, values = window.read()
    if event == "OK":
        # save input values to json file
        with open('PhotStab_input.json', 'w') as f:
            json.dump(values, f)
        # close GUI
        window.close()
        # run engine
        engine.execute(values)

    if event == "Import values from json file":
        # open file selection window
        filename = sg.popup_get_file('Select json file', file_types=(("json Files", "*.json"),))
        # import values from json file
        with open(filename, 'r') as f:
            values = json.load(f)
            window["-IN-"].update(values["-IN-"])
            window["-OUT-"].update(values["-OUT-"])
            window["-TFINAL-"].update(values["-TFINAL-"])
            window["-TCYCLE-"].update(values["-TCYCLE-"])
            window["-MINWL-"].update(values["-MINWL-"])
            window["-MAXWL-"].update(values["-MAXWL-"])
            window["-RES-"].update(values["-RES-"])
            window["-TITLE-"].update(values["-TITLE-"])
            window["-FILENAME-"].update(values["-FILENAME-"])
            window["-MINWLZOOM-"].update(values["-MINWLZOOM-"])
            window["-MAXWLZOOM-"].update(values["-MAXWLZOOM-"])
            window["-MAXABSZOOM-"].update(values["-MAXABSZOOM-"])
            window["-INSET-"].update(values["-INSET-"])
            window["-INSETWL-"].update(values["-INSETWL-"])
            window["-LABEL-FONT-SIZE-"].update(values["-LABEL-FONT-SIZE-"])
            window["-TICK-FONT-SIZE-"].update(values["-TICK-FONT-SIZE-"])
            window["-TITLE-FONT-SIZE-"].update(values["-TITLE-FONT-SIZE-"])
            window["-LEGEND-FONT-SIZE-"].update(values["-LEGEND-FONT-SIZE-"])
            if [values["-ABS-SPEC-OVERLAY-"]] == "y":
                window["-ABS-SPEC-OVERLAY-"].update("y")
            if [values["-DARK-CONTROL-"]] == "y":
                window["-DARK-CONTROL-"].update("y")
            if [values["-MULTIPLY-"]] == "y":
                window["-MULTIPLY-"].update("y")
                window["-MULTIPLY-FACTOR-"].update(values["-MULTIPLY-FACTOR-"])
            if [values["-DARK-CONTROL-"]] == "y":
                window["-DARK-CONTROL-"].update("y")
                window["-DARK-CONTROL-WLS-"].update(values["-DARK-CONTROL-WLS-"])

    if event == sg.WIN_CLOSED:
        print("ERROR: No input file selected.")
        sys.exit()
        break
