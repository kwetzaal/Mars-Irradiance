import numpy as np
import matplotlib.pyplot as plt

from Misc import csv_reader
from Misc import zenith_format

'''
checklist before running:
    - is data formatted correctly? (heatmap or time)
    - is mode set correctly? (heatmap or time)
'''

def DHI_calc(ghi, dni, zenith_ang):
    # cycles through each 2D array and calculates surface irradiance 
    i = 0
    dhi = []
    while i < len(ghi):
        row = []
        j = 0
        while j < len(ghi[i]):
            # does DHI calculations for each value
            row.append(float(ghi[i][j] - dni[i][j] * np.cos(zenith_ang[i][j]))) # NREL Solar Resource Glossary (Global Horizzontal Radiation)
            j += 1
            if j == len(ghi[i]):
                dhi.append(row)
                break
        i += 1
    return dhi

def DHI_calc_time(ghi, dni, zenith_ang):
    # time as x, irradiance as y
    i = 0
    dhi_and_time = []
    time = []
    dhi = []
    while i < len(ghi):
        time.append(ghi[0][1])
        dhi.append(float(ghi[1][i] - dni[1][i] * np.cos(zenith_ang[1][i]))) # NREL Solar Resource Glossary (Global Horizzontal Radiation)
        i += 1
    dhi_and_time.append(time)
    dhi_and_time.append(dhi)
    return dhi_and_time


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

    # mode = 0: heatmap
    # mode = 1: irradance vs. time
    mode = 0

    if mode == 0:
        dhi_irr = DHI_calc(ghi_data, dni_data, z_rad)
        print(dhi_irr)

    elif mode == 1:
        dhi_irr_time = DHI_calc_time(ghi_data, dni_data, z_rad)
        print(dhi_irr_time)

if __name__ == "__main__":
    main()

