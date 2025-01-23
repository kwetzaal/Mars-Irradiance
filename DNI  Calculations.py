import numpy as np
import matplotlib.pyplot as plt

def TOA_irradiance(solar_long):
    #initializes constants
    mean_irr = 588.6
    eccentricity = 0.0934
    Ls_p = np.deg2rad(251)

    #calcculates TOA irradiance 
    toa = mean_irr*((1 + (eccentricity * np.cos(solar_long-Ls_p))/(1-(eccentricity**2)))**2)
    return toa

def surf_irradiance(optical_depth, zenith_ang, TOA):
    #cycles through each 2D array and calculates surface irradiance 
    i = 0
    surf_irr = []
    while i < len(optical_depth):
        row = []
        j = 0
        while j < len(optical_depth[i]):
            row.append(float(round(TOA * np.cos(zenith_ang[i][j]) * (np.exp(-optical_depth[i][j])), 6)))
            j += 1
            if j == len(optical_depth[i]):
                surf_irr.append(row)
                break
        i += 1
    return surf_irr

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

    #grabs and formats optical depth data
    optical_depth = input(str("Optical Depth Data (.csv): "))
    op_data = csv_reader(optical_depth)

    #solar longitude input for TOA calculations
    solar_long = np.deg2rad(int(input("Solar Longitude: ")))
    toa = TOA_irradiance(solar_long)

    dni_irr = surf_irradiance(op_data, z_rad, toa)

    heatmap_vis(dni_irr)

    #saves data as a csv file
    a = np.asarray(dni_irr)
    np.savetxt("180_dni.csv", a, delimiter=",")
    

    

if __name__ == "__main__":
    main()