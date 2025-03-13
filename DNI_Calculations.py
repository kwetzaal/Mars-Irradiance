import numpy as np
import matplotlib.pyplot as plt

from Misc import csv_reader
from Misc import zenith_format

'''
checklist before running:
    - is data formatted correctly? (heatmap or time)
    - is mode set correctly? (heatmap or time)
'''

def DNI_calc(solar_long, optical_depth, zenith_ang):
    # initialize values
    mean_irr = 588.6
    eccentricity = 0.0934
    Ls_p = np.deg2rad(251)

    #calculates Top of Atmosphere irradiance 
    toa = mean_irr*((1 + (eccentricity * np.cos(solar_long-Ls_p))/(1-(eccentricity**2)))**2) #Altered Eq 2 (Delagodo-Baonal, et al 2016)

    #calculates Direct Normal Irradiance irradiation
    i = 0
    surf_irr = []
    while i < len(optical_depth):
        row = []
        j = 0
        while j < len(optical_depth[i]):
            # does DNI calculations for each value
            row.append(float(round(toa * np.cos(zenith_ang[i][j]) * (np.exp(-optical_depth[i][j]/np.cos(zenith_ang[i][j]))), 6))) #Eq 4 (Delagodo-Baonal, et al 2016)
            j += 1
            if j == len(optical_depth[i]):
                surf_irr.append(row)
                break
        i += 1

    return surf_irr

def DNI_calc_time(solar_long, optical_depth, zenith_ang):
    # initialize values
    mean_irr = 588.6
    eccentricity = 0.0934
    Ls_p = np.deg2rad(251)

    #calculates Top of Atmosphere irradiance 
    toa = mean_irr*((1 + (eccentricity * np.cos(solar_long-Ls_p))/(1-(eccentricity**2)))**2) #Altered Eq 2 (Delagodo-Baonal, et al 2016)

    #calculates Direct Normal Irradiance irradiation
    i = 0
    surf_irr = []
    time = []
    surf_irr_and_time = []

    while i < len(optical_depth[0]):
        time.append(optical_depth[0][i])
        surf_irr.append(float(round(toa * np.cos(zenith_ang[1][i]) * (np.exp(-optical_depth[1][0]/np.cos(zenith_ang[1][i])), 6)))) #Eq 4 (Delagodo-Baonal, et al 2016)
        i += 1
    surf_irr_and_time.append(time)
    surf_irr_and_time.append(surf_irr)

    return surf_irr_and_time

#### testing code for the function file ####

def main():
    #grabs and formats data for solar zenith angle
    zenith = input("Zenith Angle Data (.csv): ")
    z_data = csv_reader(zenith)
    z_rad = zenith_format(z_data)
    print(len(z_rad))

    #grabs and formats optical depth data
    optical_depth = input(str("Optical Depth Data (.csv): "))
    op_data = csv_reader(optical_depth)
    print(len(op_data))

    #solar longitude input for TOA calculations
    solar_long = np.deg2rad(int(input("Solar Longitude: ")))
    
    # mode = 0: heatmap
    # mode = 1: irradance vs. time
    mode = 1

    if mode == 0:
        dni_irr = DNI_calc(solar_long, op_data, z_rad)
        print(dni_irr)

    elif mode == 1:
        dni_irr_time = DNI_calc_time(solar_long, op_data, z_rad)
        print(dni_irr_time)

if __name__ == "__main__":
    main()