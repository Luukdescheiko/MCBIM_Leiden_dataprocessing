import numpy as np
import os
import matplotlib.pyplot as plt
from tkinter import *
import pandas as pd
from datetime import datetime as dt
from scipy.optimize import curve_fit
import scienceplots
import json
import FileOperations
import shutil

plt.style.use(['science', 'nature', 'no-latex'])


# ------ DEFINE FITTING CURVES ------ #
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# define fitting curves
def logistic(x, a, b, c, d):
    return a / (1 + np.exp(-b * (x - c))) + d


# define hill-langmuir function for fitting
def hill(x, START, END, n, K):
    return START + (END - START) * x ** n / (K ** n + x ** n)


def execute(values):
    path = str(values["-IN-"])
    outpath = str(values["-OUT-"])
    species = str(values["-SPECIES-"])
    c_TDR = float(values["-C-TDR-MOLAR-"])
    TDR = str(values["-SPECIES-"])
    V = float(values["-V-REACTOR-L-"])
    t_start = str(values["-T-START-"])
    t_light = str(values["-T-LIGHT-"])
    t_end = str(values["-T-END-"])
    force_end = str(values["-FORCE-END-"])
    if force_end == "y":
        force_end_time = float(values["-FORCE-END-TIME-"])
    filename = str(values["-FILENAME-"])
    sensorname = str(values["-SENSOR-NAME-"])
    title = str(values["-TITLE-"])
    showfit = str(values["-SHOW-FIT-"])
    include_dark = str(values["-INCLUDE-DARK-"])
    fittype = str(values["-FIT-TYPE-"])
    h2o2 = str(values["-H2-O2-"])
    yaxis = str(values["-Y-AXIS-"])
    ymax = values["-YMAX-"]
    ymin = values["-YMIN-"]
    V_m = float(values["-V-M-"])
    n_e = float(values["-N-E-"])
    if ymin > ymax:
        # swap the values
        ymin, ymax = ymax, ymin
    change_y_limits = str(values["-CHANGE-Y-LIMITS-"])

    if fittype == "Hill-Langmuir":
        fitfunction = hill
        p0 = [0, 1, 0, 1]

    if fittype == "logistic":
        fitfunction = logistic
        p0 = [0, 1, 0, 1]

    if TDR == "cat" or "CAT":
        ylabel2 = "TON (cat)"

    if TDR == "PS":
        ylabel2 = "TON (PS)"

    if h2o2 == "H2":
        if yaxis == "μL":
            ylabel = "$H_{2}$ (μL)"
        if yaxis == "μmol":
            ylabel = "$H_{2}$ (μmol)"

    if h2o2 == "CO":
        if yaxis == "μL":
            ylabel = "$CO$ (μL)"
        if yaxis == "μmol":
            ylabel = "$CO$ (μmol)"

    if h2o2 == "O2":
        if yaxis == "μL":
            ylabel = "$O_{2}$ (μL)"
        if yaxis == "μmol":
            ylabel = "$O_{2}$ (μmol)"

    # Import the data from the xlsx file
    data = pd.read_excel(path, sheet_name=0)

    # select and show start and end point
    startTime = t_start
    endTime = t_end
    print('startTime = %s, endTime = %s' % (startTime, endTime))

    # select data from the start point to the end point
    data = data[data['Time (YYYY-MM-DD hh:mm:ss)'] >= startTime]
    data = data[data['Time (YYYY-MM-DD hh:mm:ss)'] <= endTime]
    print(data.iloc[0:5], data.iloc[-5:])

    # make a new column with the time in minutes starting from PCP.t_light
    data['Time (min)'] = (data['Time (YYYY-MM-DD hh:mm:ss)'] - dt.strptime(t_light,
                                                                           '%Y-%m-%d %H:%M:%S')).dt.total_seconds() / 60
    print(data.iloc[0:5], data.iloc[-5:])

    # make sure that the time values are floats
    data['Time (min)'] = data['Time (min)'].astype(float)

    normfactor = np.average(data[sensorname][data['Time (min)'] < 0])

    # create a new column with the normalized data
    data['Normalized'] = data[sensorname] - normfactor
    # make sure that the normalized values are floats
    data['Normalized'] = data['Normalized'].astype(float)
    # convert normalized data from volume to micromoles
    data['umol gas'] = data['Normalized'] / V_m
    # make sure that the umol gas values are floats
    data['umol gas'] = data['umol gas'].astype(float)
    # convert normalized data from micromoles to TON(TDR)
    n_TDR = c_TDR * V
    if TDR == "PS":
        data['TON(TDR)'] = data['umol gas'] / (n_TDR * 1000000) * n_e
    if TDR == "cat":
        data['TON(TDR)'] = data['umol gas'] / (n_TDR * 1000000)

    # if fittype is undefined, use logistic
    if fittype == "":
        fitfunction = logistic
        p0 = [0, 1, 0, 1]

    if include_dark == "y":
        if force_end == "y":
            # make forcefit dataframe with all times after the begin of the dark period and before force_end_time
            forcefit = data[data['Time (min)'] >= force_end_time]
            popt_gas, pcov_gas = curve_fit(fitfunction, forcefit['Time (min)'], forcefit['Normalized'], p0=p0, maxfev=100000)
            popt_TDR, pcov_TDR = curve_fit(fitfunction, forcefit['Time (min)'], forcefit['TON(TDR)'], p0=p0, maxfev=100000)
            print(
                "For gas volume fit: a = %s, b = %s, c = %s, d = %s" % (popt_gas[0], popt_gas[1], popt_gas[2], popt_gas[3]))
        if force_end == "n":
            popt_gas, pcov_gas = curve_fit(fitfunction, data['Time (min)'], data['Normalized'], p0=p0,
                                           maxfev=100000)
            popt_TDR, pcov_TDR = curve_fit(fitfunction, data['Time (min)'], data['TON(TDR)'], p0=p0,
                                           maxfev=100000)
            print(
                "For gas volume fit: a = %s, b = %s, c = %s, d = %s" % (popt_gas[0], popt_gas[1], popt_gas[2], popt_gas[3]))

    if include_dark == "n":
        if force_end == "y":
            # make forcefit dataframe with all times after 0 minutes and before force_end_time
            forcefit = data[(data['Time (min)'] >= 0) & (data['Time (min)'] <= force_end_time)]
            popt_gas, pcov_gas = curve_fit(fitfunction, forcefit['Time (min)'], forcefit['Normalized'], p0=p0,
                                           maxfev=100000)
            popt_TDR, pcov_TDR = curve_fit(fitfunction, forcefit['Time (min)'], forcefit['TON(TDR)'], p0=p0,
                                            maxfev=100000)
            print(
                "For gas volume fit: a = %s, b = %s, c = %s, d = %s" % (popt_gas[0], popt_gas[1], popt_gas[2], popt_gas[3]))

        if force_end == "n":
            # make timelight dataframe with all times after 0 minutes
            timelight = data[data['Time (min)'] >= 0]
            popt_gas, pcov_gas = curve_fit(fitfunction, timelight['Time (min)'], timelight['Normalized'], p0=p0,
                                           maxfev=100000)
            print(
                "For gas volume fit: a = %s, b = %s, c = %s, d = %s" % (popt_gas[0], popt_gas[1], popt_gas[2], popt_gas[3]))
            popt_TDR, pcov_TDR = curve_fit(fitfunction, timelight['Time (min)'], timelight['TON(TDR)'], p0=p0,
                                           maxfev=100000)
            print("For TDR fit: a = %s, b = %s, c = %s, d = %s" % (popt_TDR[0], popt_TDR[1], popt_TDR[2], popt_TDR[3]))


        # ---------------------- PLOT ---------------------- #
    if yaxis == "μL":
        y_min = 1.1 * min(data['Normalized'])
        y_max = 1.1 * max(data['Normalized'])
        y_min2 = 1.1 * min(data['TON(TDR)'])
        y_max2 = 1.1 * max(data['TON(TDR)'])

        if change_y_limits == "y":
            # check if ymin and ymax are floats
            if isfloat(ymin) and isfloat(ymax):
                y_min = float(ymin)
                y_max = float(ymax)
            if isfloat(ymin) and not isfloat(ymax):
                y_min = float(ymin)
                y_max = 1.1 * max(data['Normalized'])
            if not isfloat(ymin) and isfloat(ymax):
                y_min = 1.1 * min(data['Normalized'])
                y_max = float(ymax)
            # check if ymin and ymax are floats
            if species == "PS":
                if isfloat(ymin) and isfloat(ymax):
                    y_min2 = (float(ymin) / V_m) / (n_TDR * 1000000) * n_e
                    y_max2 = (float(ymax) / V_m) / (n_TDR * 1000000) * n_e
                if isfloat(ymin) and not isfloat(ymax):
                    y_min2 = (float(ymin) / V_m) / (n_TDR * 1000000) * n_e
                    y_max2 = 1.1 * max(data['TON(TDR)'])
                if not isfloat(ymin) and isfloat(ymax):
                    y_min2 = 1.1 * min(data['TON(TDR)'])
                    y_max2 = (float(ymax) / V_m) / (n_TDR * 1000000) * n_e

            if species == "cat":
                if isfloat(ymin) and isfloat(ymax):
                    y_min2 = (float(ymin) / V_m) / (n_TDR * 1000000)
                    y_max2 = (float(ymax) / V_m) / (n_TDR * 1000000)
                if isfloat(ymin) and not isfloat(ymax):
                    y_min2 = (float(ymin) / V_m) / (n_TDR * 1000000)
                    y_max2 = 1.1 * max(data['TON(TDR)'])
                if not isfloat(ymin) and isfloat(ymax):
                    y_min2 = 1.1 * min(data['TON(TDR)'])
                    y_max2 = (float(ymax) / V_m) / (n_TDR * 1000000)

    if yaxis == "μmol":
        plt.plot(data['Time (min)'], data['umol gas'])

        y_min = 1.1 * min(data['umol gas'])
        y_max = 1.1 * max(data['umol gas'])
        y_min2 = 1.1 * min(data['TON(TDR)'])
        y_max2 = 1.1 * max(data['TON(TDR)'])

        if change_y_limits == "y":
            # check if ymin and ymax are floats
            if isfloat(ymin) and isfloat(ymax):
                y_min = float(ymin)
                y_max = float(ymax)
            if isfloat(ymin) and not isfloat(ymax):
                y_min = float(ymin)
                y_max = 1.1 * max(data['umol gas'])
            if not isfloat(ymin) and isfloat(ymax):
                y_min = 1.1 * min(data['umol gas'])
                y_max = float(ymax)

                if change_y_limits == "y":
                    # check if ymin and ymax are floats
                    if species == "PS":
                        if isfloat(ymin) and isfloat(ymax):
                            y_min2 = (ymin / V_m) / (n_TDR * 1000000) * n_e
                            y_max2 = (ymax / V_m) / (n_TDR * 1000000) * n_e
                        if isfloat(ymin) and not isfloat(ymax):
                            y_min2 = (ymin / V_m) / (n_TDR * 1000000) * n_e
                            y_max2 = 1.1 * max(data['TON(TDR)'])
                        if not isfloat(ymin) and isfloat(ymax):
                            y_min2 = 1.1 * min(data['TON(TDR)'])
                            y_max2 = (ymax / V_m) / (n_TDR * 1000000) * n_e

                    if species == "cat":
                        if isfloat(ymin) and isfloat(ymax):
                            y_min2 = (ymin / V_m) / (n_TDR * 1000000)
                            y_max2 = (ymax / V_m) / (n_TDR * 1000000)
                        if isfloat(ymin) and not isfloat(ymax):
                            y_min2 = (ymin / V_m) / (n_TDR * 1000000)
                            y_max2 = 1.1 * max(data['TON(TDR)'])
                        if not isfloat(ymin) and isfloat(ymax):
                            y_min2 = 1.1 * min(data['TON(TDR)'])
                            y_max2 = (ymax / V_m) / (n_TDR * 1000000)

    #plt.plot(data['Time (min)'], data['Normalized'])
    plt.xlabel('Time (min)')
    plt.ylabel(ylabel)
    plt.ylim(y_min, y_max)

    # create second y-axis with the TON(PS) data
    ax2 = plt.twinx()
    ax2.plot(data['Time (min)'], data['TON(TDR)'], color='black')
    ax2.set_ylabel(ylabel2)
    ax2.set_ylim(y_min2, y_max2)

    plt.title(title)

    if include_dark == "y":
        x = np.linspace(data['Time (min)'].min(), data['Time (min)'].max(), 1000)
        if force_end == "y":
            x = np.linspace(data['Time (min)'].min(), force_end_time, 1000)

    if include_dark == "n":
        # create timelight dataframe containing all values of the light phase
        timelight = data[data['Time (min)'] >= 0]
        x = np.linspace(timelight['Time (min)'].min(), timelight['Time (min)'].max(), 1000)
        if force_end == "y":
            x = np.linspace(timelight['Time (min)'].min(), force_end_time, 1000)

    y = fitfunction(x, *popt_TDR)
    y2 = fitfunction(x, *popt_gas)

    if showfit == "y":
        plt.plot(x, y, color='red')

    # save the plot to a png file in outpath
    plt.savefig(os.path.join(outpath, filename) + '.png', dpi=600)
    plt.show()

    # data for the fit parameters
    x = data['Time (min)']
    y3 = fitfunction(x, *popt_TDR)
    y4 = fitfunction(x, *popt_gas)
    y5 = fitfunction(x, *popt_gas) / V_m

    # save the data columns of the plot to a csv file, including the fitted curves
    df = pd.DataFrame({'Time (min)': data['Time (min)'], 'uL gas': data['Normalized'], 'umol gas': data['umol gas'],
                       'TON(TDR)': data['TON(TDR)'],
                       'Fit TON(TDR)': y3, 'Fit uL gas': y4, 'Fit umol gas': y5})
    df.to_excel(os.path.join(outpath, filename) + '_data.xlsx', index=False)

    if force_end == "n":
        print('The end time was set to the end of the plot.')
        # calculate the value of the fit at the lest time point
        V_gas_end = df['Fit uL gas'].max()
        TON_TDR_end = df['Fit TON(TDR)'].max()

    if force_end == "y":
        print('The end time was forced to be t = %s min.' % force_end_time)
        # calculate the TON(PS) at the forced end time
        TON_TDR_end = fitfunction(force_end_time, *popt_TDR)
        # calculate V_O2 at the forced end time
        V_gas_end = fitfunction(force_end_time, *popt_gas)
        # zoom the x-axis from the minimum time value to the forced end time
        plt.xlim(data['Time (min)'].min(), force_end_time)

    # determine TOFmax using the saved fitting data
    df = df[df['Time (min)'] >= 0]
    # calculate TOFmax by determining the maximum slope of the curve and its time
    df['Slope'] = df['Fit TON(TDR)'].diff() / df['Time (min)'].diff()
    TOFmax = df['Slope'].max() * 60
    TOFmax_time = df.loc[df['Slope'].idxmax(), 'Time (min)']
    print('V_gas_end = %s uL' % V_gas_end)
    print('TON(TDR)_end = %s' % TON_TDR_end)
    print('TOFmax = %s h-1' % TOFmax)
    print('TOFmax_time = %s min' % TOFmax_time)

    # save V_gas_end, TON(TDR)_end, TOFmax and TOFmax_time to a csv file
    with open(os.path.join(outpath, filename + '_results') + '.csv', 'w') as f:
        f.write('V_gas_end,TON(TDR)_end,TOFmax,TOFmax_time (min), sensor name \n')  # header
        f.write('%s,%s,%s,%s,%s' % (V_gas_end, TON_TDR_end, TOFmax, TOFmax_time, sensorname))
        # write the fits including optimized parameters
        f.write('Gas fit (%s): a = %s, b = %s, c = %s, d = %s \n' % (
            fittype, popt_gas[0], popt_gas[1], popt_gas[2], popt_gas[3]))
        f.write('TDR fit (%s): a = %s, b = %s, c = %s, d = %s \n' % (
            fittype, popt_TDR[0], popt_TDR[1], popt_TDR[2], popt_TDR[3]))

    # take parameters.json and copy it to the output folder
    shutil.copyfile('parameters.json', os.path.join(outpath, filename + '_parameters') + '.json')

    print('Done!')
