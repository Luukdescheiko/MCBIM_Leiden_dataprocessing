import matplotlib.pyplot as plt
import scienceplots
import FileOperations
import glob
import pandas as pd
import os

plt.style.use(['science', 'nature', 'no-latex'])

colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

def execute(values):
    # import parameters from GUI
    inputfolder = values["-IN-"]
    ylabel = values["-Y-AXIS-"]
    gas = values["-GAS-PRODUCED-"]
    showfit = values["-SHOW-FIT-"]
    change_y_limits = values["-CHANGE-Y-LIMITS-"]
    if change_y_limits == "y":
        ymax = float(values["-YMAX-"])
        ymin = float(values["-YMIN-"])
    title = values["-TITLE-"]
    titlesize = int(values["-TITLE-FONT-SIZE-"])
    legendsize = int(values["-LEGEND-FONT-SIZE-"])
    labelsize = int(values["-LABEL-FONT-SIZE-"])
    ticksize = int(values["-TICK-FONT-SIZE-"])

    # check how many excel files are in the input folder
    files = glob.glob(os.path.join(inputfolder, "**/*.xlsx"), recursive=True)
    number_of_files = len(files)

    legendkeys = []
    for i in range(number_of_files):
        # get the legend keys from the file names until the first underscore
        legendkeys.append(os.path.basename(files[i]).split("_")[0])

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

    # create the figure
    if ylabel == "gas volume":
        for i in range(number_of_files):
            time = pd.read_excel(files[0])["Time (min)"]
            # load the data
            df = pd.read_excel(files[i])
            plt.plot(df["Time (min)"], df["uL gas"], alpha = 0.5, linewidth=2, color=colors[i], label=legendkeys[i])
            if showfit == "y":
                # make df2 starting from time 0
                df2 = df[df["Time (min)"] >= 0]
                # plot the fit with half linewidth and in same color as data starting at time 0
                plt.plot(df2['Time (min)'], df2['Fit uL gas'], linewidth=1, color=colors[i], label = '_nolegend_')

        if gas == "H2":
            plt.ylabel("$H_2$ (μL)")

        if gas == "CO":
            plt.ylabel("CO (μL)")

        if gas == "O2":
            plt.ylabel("$O_2$ (μL)")

    if ylabel == "TON":
        plt.ylabel("TON")
        for i in range(number_of_files):
            time = pd.read_excel(files[0])["Time (min)"]
            # load the data
            df = pd.read_excel(files[i])
            plt.plot(df["Time (min)"], df["TON(TDR)"], alpha = 0.5, linewidth=2, color=colors[i], label=legendkeys[i])
            if showfit == "y":
                # make df2 starting from time 0
                df2 = df[df["Time (min)"] >= 0]
                # plot the fit with half linewidth and in same color as data starting at time 0
                plt.plot(df2['Time (min)'], df2['Fit TON(TDR)'], linewidth=1, color=colors[i], label = '_nolegend_')

    if ylabel == "PTON":
        plt.ylabel("PTON")
        for i in range(number_of_files):
            time = pd.read_excel(files[0])["Time (min)"]
            # load the data
            df = pd.read_excel(files[i])
            plt.plot(df["Time (min)"], df["PTON"], alpha = 0.5, linewidth=2, color=colors[i], label=legendkeys[i])
            if showfit == "y":
                # make df2 starting from time 0
                df2 = df[df["Time (min)"] >= 0]
                # plot the fit with half linewidth and in same color as data starting at time 0
                plt.plot(df2['Time (min)'], df2['Fit PTON'], linewidth=1, color=colors[i], label = '_nolegend_')

    if ylabel == "umol":
        for i in range(number_of_files):
            time = pd.read_excel(files[0])["Time (min)"]
            # load the data
            df = pd.read_excel(files[i])
            plt.plot(df["Time (min)"], df["umol gas"], alpha = 0.5, linewidth=2, color=colors[i], label=legendkeys[i])
            if showfit == "y":
                # make df2 starting from time 0
                df2 = df[df["Time (min)"] >= 0]
                # plot the fit with half linewidth and in same color as data starting at time 0
                plt.plot(df2['Time (min)'], df2['Fit umol gas'], linewidth=1, color=colors[i], label = '_nolegend_')

            if gas == "H2":
                plt.ylabel("$H_2$ (μmol)")

            if gas == "CO":
                plt.ylabel("CO (μmol)")

            if gas == "O2":
                plt.ylabel("$O_2$ (μmol)")

    # change the y limits if the user wants to
    if change_y_limits == "y":
        plt.ylim(ymin, ymax)

    plt.title(title)
    # add legend to the plot using the colors and legendlabels. Use every second color
    plt.legend(legendkeys, loc = 'upper left')
    plt.xlabel("Time (min)")
    # save the plot in input folder
    plt.savefig(os.path.join(inputfolder, "%s_plot.png" % ylabel), dpi=600)

    # show the plot
    plt.show()
