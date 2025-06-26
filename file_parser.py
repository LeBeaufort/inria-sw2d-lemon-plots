class InvalidInputFileError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def ResultHydro_parser(filename):
    file = open(filename, "r")

    mesh_data = {}
    first_line = file.readline().split()

    if len(first_line) != 7:
        print("[WARN] Number of entry is different than 7")
        if len(first_line) == 3:
            print("[WARN] the input file may be a ProbeTimeSeries file")

    # create keys with file headers
    for k in first_line: mesh_data[k] = []

    key_list = list(mesh_data.keys())
    for line in file:
        for value, key in zip(line.split(), key_list):
            mesh_data[key].append(float(value))

    return mesh_data

def probe_parser(filename):

    probe_list = []
    data = {}

    file = open(filename, "r")

    if file.readline() != 3:
        raise InvalidInputFileError("The file contains no probe or it is not a ProbeTimeSeries file")

    for line in file:
        l = line.split()

        if len(l) == 3: # if yes, the line describe a probe
            probe_list.append(l[0]) # the first part of this line will be the name of the probe
        else:
            if not data.keys():
                for k in l: data[k] = [] # create keys of data based on the first line of more than 3 parts
            else:
                for value, key in zip(line.split(), data.keys()):
                    data[key].append(float(value))

    return [probe_list, data]

