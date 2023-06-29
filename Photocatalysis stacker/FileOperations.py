import json


def read_file_as_parameters(paramfile):
    with open(paramfile, 'r') as f:
        parameters = json.load(f)
    return parameters


def write_parameters_as_file(outpath, parameters):
    with open(outpath, 'w') as f:
        json.dump(parameters, f)
