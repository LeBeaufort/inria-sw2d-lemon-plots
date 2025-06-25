def ResultHydro_parser(filename):
    file = open(filename, "r")

    mesh_data = {}

    # create keys with file headers
    for k in file.readline().split(): mesh_data[k] = []

    key_list = list(mesh_data.keys())
    for line in file:
        for value, key in zip(line.split(), key_list):
            mesh_data[key].append(float(value))

    return mesh_data

def probe_parser(filename):

    probe_list = []
    data = {}


    file = open(filename, "r")

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

