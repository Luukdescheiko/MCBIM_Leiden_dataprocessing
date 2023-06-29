# import required packages
import os
import sys
import numpy as np
import json
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import patches as mpatches
import scienceplots
import sys
import PySimpleGUI as sg

plt.style.use(['science', 'nature', 'no-latex'])

def execute(values):
    color = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22",
             "#17becf"]
    # import values from GUI
    tfinal = float(values['-TFINAL-'])
    tcycle = float(values['-TCYCLE-'])
    minwl = float(values['-MINWL-'])
    maxwl = float(values['-MAXWL-'])
    resolution = float(values['-RES-'])
    minwlzoom = float(values['-MINWLZOOM-'])
    maxwlzoom = float(values['-MAXWLZOOM-'])
    maxabszoom = float(values['-MAXABSZOOM-'])
    inset = values['-INSET-']
    title = values['-TITLE-']
    path = values['-IN-']
    outpath = values['-OUT-']
    insetwl = values['-INSETWL-'].split(',')
    filename = values['-FILENAME-']
    titlesize = int(values['-TITLE-FONT-SIZE-'])
    labelsize = int(values['-LABEL-FONT-SIZE-'])
    ticksize = int(values['-TICK-FONT-SIZE-'])
    legendsize = int(values['-LEGEND-FONT-SIZE-'])
    absspecoverlay = values['-ABS-SPEC-OVERLAY-']
    darkcontrol = values['-DARK-CONTROL-']
    darkcontrolwls = values['-DARK-CONTROL-WLS-'].split(',')
    multiplyabs = values['-MULTIPLY-']
    multiplyabsfactor = float(values['-MULTIPLY-FACTOR-'])

    # save input values to json file in output folder
    with open(os.path.join(outpath, 'PhotStab_input.json'), 'w') as f:
        json.dump(values, f)

    # n, needed for dataframe slicing, DO NOT CHANGE
    n = int(2 + (maxwl - minwl) / resolution)

    cycles = int(tfinal / tcycle + 1)

    # import csv file
    data = pd.read_csv(path)

    # color gradient for plots
    cmap = mpl.cm.get_cmap('seismic')

    # create new dataframes with only wavelengths and absorbance of all samples
    df = data.iloc[1:n:1]
    #make sure values in df are floats
    df = df.astype(float)
    # change the font size of the axis labels
    plt.rcParams.update({'font.size': titlesize})
    # change the font size of the legend
    plt.rcParams.update({'legend.fontsize': legendsize})
    # change the font size of the numbers on the axis
    plt.rcParams.update({'axes.labelsize': labelsize})
    # change the font size of the numbers on the axis
    plt.rcParams.update({'xtick.labelsize': ticksize})
    # change the font size of the numbers on the axis
    plt.rcParams.update({'ytick.labelsize': ticksize})
    Wavelength = np.array(df.iloc[:, 0], dtype=float)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Absorbance')
    plt.title(title)

    for i in range(cycles):
        Absorbance = np.array(df.iloc[:, int(1 + 2 * i)], dtype=float)
        plt.plot(Wavelength, Absorbance, label=(str(i * tcycle) + " min"), color=cmap(i / cycles))

    # plot abs if selected
    if absspecoverlay == "y":
        # select file using GUI and import data, use a plot that has been processed using the UV-Vis.py script!
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        data_absdf = pd.read_csv(file_path)
        Wavelengthabs = np.array(data_absdf.iloc[:, 1], dtype=float)
        Absorbanceabs = np.array(data_absdf.iloc[:, 2], dtype=float)
        if multiplyabs == "y":
            Absorbanceabs = Absorbanceabs * multiplyabsfactor
        plt.plot(Wavelengthabs, Absorbanceabs, color="black", linestyle='dashed')

    # ask if plot needs to be zoomed in
    plt.xlim(minwlzoom, maxwlzoom)
    plt.ylim(0, maxabszoom)

    # make a legend featuring only the first two and last two cycles
    legend1 = mpatches.Patch(color=cmap(0), label='0 min')
    legend2 = mpatches.Patch(color=cmap((cycles - 2) / cycles), label=str(tfinal) + " min")
    plt.legend(handles=[legend1, legend2], loc='upper right')

    # make inset plot of absorbance at specified wavelength over time
    if inset == "y":
        wlintegers = Wavelength.astype(int)
        # plot absorbance at specified wavelength over time in inset plot
        plt.axes([0.55, 0.45, 0.25, 0.25])
        plt.xlabel('Time (min)')
        plt.ylabel('Absorbance')
        # Create pandas dataframe with timepoints (in minutes)
        time = np.arange(0, tfinal + tcycle, tcycle)
        dfinset = pd.DataFrame({'Time': time})
        for i in range(len(insetwl)):
            # find index of wavelengths in Wavelength array and make a list of them
            insetindexes = np.where(wlintegers == int(insetwl[i]))
            # convert list to integer
            insetindex = insetindexes[0][0]
            # create array with absorbance at specified wavelength
            insetabs = []
            for j in range(cycles):
                insetabs.append(df.iloc[insetindex, 2 * j + 1])
            # create array with time
            time = np.arange(0, tfinal + tcycle, tcycle)
            plt.plot(time, insetabs, color=color[i])
            # add text with absorbance at specified wavelength at end of cycle
            plt.text(tfinal, insetabs[-1], "$A_{%s}$" % (insetwl[i]))
            plt.xlim(0, tfinal)
            # append the last column of insetabs to dfinset
            dfinset.insert(i + 1, "A_" + insetwl[i], insetabs)
        if darkcontrol == "y":
            # ask for dark control file
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename()
            data = pd.read_csv(file_path)
            # remove first row
            data_dark = data.iloc[1:n:1]
            # make sure values in df are floats
            data_dark = data_dark.astype(float)
            # create new dataframe with only wavelengths and absorbance of dark control
            darkwls = np.array(data_dark.iloc[:, 0], dtype=float)
            darkwlsintegers = darkwls.astype(int)
            # find index of wavelengths in Wavelength array and make a list of them
            for i in range(len(darkcontrolwls)):
                darkindexes = np.where(darkwlsintegers == int(darkcontrolwls[i]))
                # convert list to integer
                darkindex = darkindexes[0][0]
                # create array with absorbance at specified wavelength
                darkabs = []
                for j in range(cycles):
                    darkabs.append(data_dark.iloc[darkindex, 2 * j + 1])
                # create array with time
                time = np.arange(0, tfinal + tcycle, tcycle)
                plt.plot(time, darkabs, color='black')
                # print
                plt.text(tfinal, darkabs[-1], "$A_{%s}$ dark" % (darkcontrolwls[i]))
                plt.xlim(0, tfinal)

    # Ask if user wants to save the plot
    plt.savefig(os.path.join(outpath, filename + ".png"), dpi=600)
    print("Plot saved as %s" % filename + ".png")

    # show plot
    plt.show()

    # slice df by cutting every other column starting from the third column. Include the zeroth column
    df = df.iloc[0:, 1:2 * cycles:2]
    # insert a column with the wavelength values
    df.insert(0, "Wavelength", Wavelength)

    # save a csv file with the data from the plot to the output folder
    df.to_csv(os.path.join(outpath, str(filename + ".csv")), index=False)

    # save a csv file with the data from the inset plot to the output folder
    dfinset.to_csv(os.path.join(outpath, str(filename + "_inset.csv")), index=False)
    print("Data saved!")

    print('DONE')

    sys.exit()
