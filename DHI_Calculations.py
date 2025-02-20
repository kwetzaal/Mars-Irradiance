import numpy as np
import matplotlib.pyplot as plt

def DHI_calc(ghi, dni, zenith_ang):
    #cycles through each 2D array and calculates surface irradiance 
    i = 0
    dhi = []
    while i < len(ghi):
        row = []
        j = 0
        while j < len(ghi[i]):
            row.append(float(ghi[i][j] - dni[i][j] * np.cos(zenith_ang[i][j])))
            j += 1
            if j == len(ghi[i]):
                dhi.append(row)
                break
        i += 1
    return dhi

def csv_reader(dataset):
    #grabs data from csv file 
    data = np.genfromtxt(dataset, dtype = float, delimiter = ',')

    count = 0
    for i in data[0]:
        count += 1

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

def heatmap_vis(data):
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
    cbar.set_label('Direct Normal Irradiance (W/m^2)', fontsize=12)

    #more labeling
    plt.title("MCD Incident Horizontal Irradiance")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    plt.show(block=True)

def main():
    #grabs and formats data for solar zenith angle
    zenith = input("Zenith Angle Data (.csv): ")
    z_data = csv_reader(zenith)

    #if solar zenith ang is more than 90 deg, it is not usable
    z_val = []
    for i in z_data:
        row = []
        for j in i:
            if j > 90:
                row.append(90)
                continue
            row.append(j)
        z_val.append(row)

    #turns into rad for calculations
    z_rad = np.deg2rad(z_val)
    print(len(z_rad))

    #grabs and formats GHI data
    ghi = input(str("GHI Data (.csv): "))
    ghi_data = csv_reader(ghi)
    print(len(ghi_data))

    #grabs and formats DNI data
    dni = input(str("DNI Data (.csv): "))
    dni_data = np.genfromtxt(dni, dtype = float, delimiter = ',')
    print(len(dni_data))

    dhi_irr = DHI_calc(ghi_data, dni_data, z_rad)

    #produces heatmap
    heatmap_vis(dhi_irr)

    #saves data as a csv file
    a = np.asarray(dhi_irr)
    np.savetxt("180_dhi.csv", a, delimiter=",")

if __name__ == "__main__":
    main()