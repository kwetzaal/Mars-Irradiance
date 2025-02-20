import numpy as np
import matplotlib.pyplot as plt

# Hello world
def csv_reader(dataset):
    #grabs data from csv file 
    data = np.genfromtxt(dataset, dtype = float, delimiter = ',')

    count = len(data[0])
    if count == 64:
        return data
    else:
        #flips the rows and columns in the csv file data (becomes longitude vs. lat)
        new_data = []
        new_row = []
        row = 0
        value = 0
        while row < len(data):
            new_row.append(float(data[row][value]))
            row += 1
            if row == len(data):
                new_data.append(new_row)
                value += 1
                if value == count:
                    break
                else:
                    new_row = []
                    row = 0
            else:
                continue
            
        return(new_data)

def zenith_format(zenith):
    #if solar zenith ang is more than 90 deg, it is not usable
    z_val = []
    for i in zenith:
        row = []
        for j in i:
            if j > 90:
                row.append(90)
                continue
            row.append(j)
        z_val.append(row)

    #turns into rad for calculations
    z_rad = np.deg2rad(z_val)
    return(z_rad)

def heatmap_vis(data, cbar_label, title):
    #sets the bounds of longitude and latitude
    left = -180
    right = 180
    bottom = -90
    top = 90
    extent = [left, right, bottom, top]

    #creates graph
    plt.imshow(data, interpolation='nearest', extent=extent)

    #initializes and labels color bar
    cbar = plt.colorbar()
    cbar.set_label(cbar_label, fontsize=12)

    #more labeling
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    plt.show(block=True)





