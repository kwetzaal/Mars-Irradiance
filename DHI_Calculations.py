import numpy as np
import matplotlib.pyplot as plt

from Misc import csv_reader
from Misc import zenith_format

def DHI_calc(ghi, dni, zenith_ang):
    # cycles through each 2D array and calculates surface irradiance 
    i = 0
    dhi = []
    while i < len(ghi):
        row = []
        j = 0
        while j < len(ghi[i]):
            # does DHI calculations for each value
            row.append(float(ghi[i][j] - dni[i][j] * np.cos(zenith_ang[i][j])))
            j += 1
            if j == len(ghi[i]):
                dhi.append(row)
                break
        i += 1
    return dhi


#### testing code for the function file ####

def main():
    #grabs and formats data for solar zenith angle
    zenith = input("Zenith Angle Data (.csv): ")
    z_data = csv_reader(zenith)
    z_rad = zenith_format(z_data)
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
    print(dhi_irr)

if __name__ == "__main__":
    main()

