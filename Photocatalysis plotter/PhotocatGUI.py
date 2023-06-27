import os
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import FileOperations
import engine
import sys

plt.style.use(['science', 'nature', 'no-latex'])

# ----- Define option menus ----- #
fittype = ["Hill-Langmuir", "logistic"]
species = ["PS", "cat"]
h2o2 = ["H2", "O2", "CO"]
y_n = ["y", "n"]
y_axis_units = ["μL", "μmol"]
V_M = ["24.5", "22.4"]

# ----- Define GUI ----- #
layout = [
    [sg.Text("Input File:"), sg.Input(key="-IN-"), sg.FileBrowse(file_types=(("Excel Files", "*.xls*"),))],
    [sg.Text("Output Folder:"), sg.Input(key="-OUT-"), sg.FolderBrowse()],
    [sg.Text("Molar volume:"), sg.InputOptionMenu(V_M, key="-V-M-")],
    [sg.Text("y-axis unit"), sg.InputOptionMenu(y_axis_units, key="-Y-AXIS-")],
    [sg.Text("TON-determining reagent:"), sg.InputOptionMenu(species, key="-SPECIES-")],
    [sg.Text("If PS, what is n_e?:"), sg.InputOptionMenu(fittype, key="-N-E-")],
    [sg.Text("Concentration of TON-determining reagent in M:", enable_events=True), sg.Input(key="-C-TDR-MOLAR-")],
    [sg.Text("Reactor Volume in L:"), sg.Input(key="-V-REACTOR-L-")],
    [sg.Text("Are you making O2 or H2?"), sg.InputOptionMenu(h2o2, key="-H2-O2-")],
    [sg.Text("Start of dark period YYYY-MM-DD HH:MM:SS"), sg.Input(key="-T-START-")],
    [sg.Text("Start of light period YYYY-MM-DD HH:MM:SS"), sg.Input(key="-T-LIGHT-")],
    [sg.Text("End of experiment YYYY-MM-DD HH:MM:SS"), sg.Input(key="-T-END-")],
    [sg.Text("Do you want to force the end time of the fit (y/n)?"), sg.InputOptionMenu(y_n, key="-FORCE-END-")],
    [sg.Text("If yes, what time (min)?"), sg.Input(key="-FORCE-END-TIME-")],
    [sg.Text("Enter Filename"), sg.Input(key="-FILENAME-")],
    [sg.Text("Sensor name FROM XLSX FILE!"), sg.Input(key="-SENSOR-NAME-")],
    [sg.Text("Which fit type do you want?"), sg.InputOptionMenu(fittype, key="-FIT-TYPE-")],
    [sg.Text("Do you want to include dark period in the fit (exclude if bad fit)?"),
     sg.InputOptionMenu(y_n, key="-INCLUDE-DARK-")],
    [sg.Text("Do you want to show the fit (y/n)?"), sg.InputOptionMenu(y_n, key="-SHOW-FIT-")],
    [sg.Text("Do you want to adjust the y-axis limits? (y/n)?"), sg.InputOptionMenu(y_n, key="-CHANGE-Y-LIMITS-")],
    [sg.Text("Maximum y-axis value (μL or μmol):"), sg.Input(key="-YMAX-")],
    [sg.Text("Minimum y-axis value (μL or μmol):"), sg.Input(key="-YMIN-")],
    [sg.Text("Enter Title:"), sg.Input(key="-TITLE-")],
    [sg.Exit(), sg.Button("Calculate and Plot"), sg.Button("Import json file")]
]

# ----- Create the window ----- #
window = sg.Window("Photocatalysis plotter & calculator", layout)
window.Finalize()
# load the parameters from the last run
if os.path.exists("parameters.json"):
    parameters = FileOperations.read_file_as_parameters("parameters.json")
    window["-IN-"].update(parameters["-IN-"])
    window["-OUT-"].update(parameters["-OUT-"])
    window["-SPECIES-"].update(parameters["-SPECIES-"])
    window["-C-TDR-MOLAR-"].update(parameters["-C-TDR-MOLAR-"])
    window["-V-REACTOR-L-"].update(parameters["-V-REACTOR-L-"])
    try:
        window["-Y-AXIS-"].update(parameters["-Y-AXIS-"])
    except:
        pass
    try:
        window["-V-M-"].update(parameters["-V-M-"])
    except:
        pass
    window["-H2-O2-"].update(parameters["-H2-O2-"])
    window["-T-START-"].update(parameters["-T-START-"])
    window["-T-LIGHT-"].update(parameters["-T-LIGHT-"])
    window["-T-END-"].update(parameters["-T-END-"])
    window["-FORCE-END-"].update(parameters["-FORCE-END-"])
    window["-FORCE-END-TIME-"].update(parameters["-FORCE-END-TIME-"])
    window["-FILENAME-"].update(parameters["-FILENAME-"])
    window["-SENSOR-NAME-"].update(parameters["-SENSOR-NAME-"])
    window["-INCLUDE-DARK-"].update(parameters["-INCLUDE-DARK-"])
    window["-FIT-TYPE-"].update(parameters["-FIT-TYPE-"])
    window["-SHOW-FIT-"].update(parameters["-SHOW-FIT-"])
    window["-CHANGE-Y-LIMITS-"].update(parameters["-CHANGE-Y-LIMITS-"])
    window["-TITLE-"].update(parameters["-TITLE-"])
    window["-N-E-"].update(parameters["-N-E-"])

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WINDOW_CLOSED, "Exit"):
        sys.exit()
    if event == "Calculate and Plot":
        # Save parameters as a json file to outpath
        FileOperations.write_parameters_as_file("parameters.json", values)
        window.close()
        engine.execute(values)
    if event == "Import json file":
        # open dialog box to select the json file
        filename = sg.popup_get_file('Select the json file', no_window=True)
        # load the parameters from the json file
        parameters = FileOperations.read_file_as_parameters(filename)
        # update the parameters in the GUI
        # if the parameters are not in the json file, use the default values
        if "-IN-" in parameters:
            window["-IN-"].update(parameters["-IN-"])
        if "-OUT-" in parameters:
            window["-OUT-"].update(parameters["-OUT-"])
        if "-SPECIES-" in parameters:
            window["-SPECIES-"].update(parameters["-SPECIES-"])
        if "-C-TDR-MOLAR-" in parameters:
            window["-C-TDR-MOLAR-"].update(parameters["-C-TDR-MOLAR-"])
        if "-V-REACTOR-L-" in parameters:
            window["-V-REACTOR-L-"].update(parameters["-V-REACTOR-L-"])
        if "-H2-O2-" in parameters:
            window["-H2-O2-"].update(parameters["-H2-O2-"])
        if "-T-START-" in parameters:
            window["-T-START-"].update(parameters["-T-START-"])
        if "-T-LIGHT-" in parameters:
            window["-T-LIGHT-"].update(parameters["-T-LIGHT-"])
        if "-T-END-" in parameters:
            window["-T-END-"].update(parameters["-T-END-"])
        if "-FORCE-END-" in parameters:
            window["-FORCE-END-"].update(parameters["-FORCE-END-"])
        if "-FORCE-END-TIME-" in parameters:
            window["-FORCE-END-TIME-"].update(parameters["-FORCE-END-TIME-"])
        if "-FILENAME-" in parameters:
            window["-FILENAME-"].update(parameters["-FILENAME-"])
        if "-SENSOR-NAME-" in parameters:
            window["-SENSOR-NAME-"].update(parameters["-SENSOR-NAME-"])
        if "-INCLUDE-DARK-" in parameters:
            window["-INCLUDE-DARK-"].update(parameters["-INCLUDE-DARK-"])
        if "-FIT-TYPE-" in parameters:
            window["-FIT-TYPE-"].update(parameters["-FIT-TYPE-"])
        if "-FIT-TYPE-" not in parameters:
            window["-FIT-TYPE-"].update("logistic")
        if "-SHOW-FIT-" in parameters:
            window["-SHOW-FIT-"].update(parameters["-SHOW-FIT-"])
        if "-YMAX-" in parameters:
            window["-YMAX-"].update(parameters["-YMAX-"])
        if "-YMIN-" in parameters:
            window["-YMIN-"].update(parameters["-YMIN-"])
        if "-TITLE-" in parameters:
            window["-TITLE-"].update(parameters["-TITLE-"])
        if "-CHANGE-Y-LIMITS-" in parameters:
            window["-CHANGE-Y-LIMITS-"].update(parameters["-CHANGE-Y-LIMITS-"])
        if "-V-M-" in parameters:
            window["-V-M-"].update(parameters["-V-M-"])
        if "-Y-AXIS-" in parameters:
            window["-Y-AXIS-"].update(parameters["-Y-AXIS-"])
        if "-N-E-" in parameters:
            window["-N-E-"].update(parameters["-N-E-"])

# terminate the program
root.mainloop()
sys.exit()
