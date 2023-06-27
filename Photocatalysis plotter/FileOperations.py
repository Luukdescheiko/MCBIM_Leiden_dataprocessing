import json


def read_file_as_parameters(paramfile):
    with open(paramfile, 'r') as f:
        parameters = json.load(f)
        if "-FIT-TYPE-" not in parameters:
            parameters["-FIT-TYPE-"] = "logistic"
        if "-YMAX-" not in parameters:
            parameters["-YMAX-"] = ""
        if "-YMIN-" not in parameters:
            parameters["-YMIN-"] = ""
        if "-CHANGE-Y-LIMITS-" not in parameters:
            parameters["-CHANGE-Y-LIMITS-"] = "n"
        if "-V-M-" not in parameters:
            # open a popup option menu to select the molar volume
            parameters["-V-M-"] = "24.5"

    return parameters


def write_parameters_as_file(outpath, parameters):
    with open(outpath, 'w') as f:
        json.dump(parameters, f)
