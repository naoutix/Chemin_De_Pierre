import numpy as np

def read_file(filename):
    """ Read coord file """
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    x, y, z = [], [], []

    for line in lines:
        coord = line.split(" ")
        x.append(float(coord[0]))
        y.append(float(coord[1]))
        z.append(float(coord[2]))

    shape = (int(np.sqrt(len(x))), int(np.sqrt(len(x))))

    x = np.array(x).reshape(shape)
    y = np.array(y).reshape(shape)
    z = np.array(z).reshape(shape)

    return x, y, z