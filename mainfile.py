import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from Misc import zenith_format
from DNI_Calculations import DNI_calc
from DHI_Calculations import DHI_calc

from Misc import csv_reader

def main():
    valid2 = False
    while valid2 == False:
        # error checker for zenith angle data input
        valid = False
        while not valid:
            try:
                zenith = input("Zenith Angle Data (.csv): ")
                z_data = csv_reader(zenith)
                z_rad = zenith_format(z_data)
                valid = True
            except:
                print("Error: File not found. Please try again.") # if zenith cannot be found as a csv file, return error

        # error checker for optical depth data input
        valid = False
        while not valid:
            try:
                optical_depth = input(str("Optical Depth Data (.csv): "))
                op_data = csv_reader(optical_depth)
                valid = True
            except:
                print("Error: File not found. Please try again.") # if optical depth canot be found as a csv file, return error

        # error checker for solar longitude input
        valid = False
        while not valid:
            try:
                solar_long = np.deg2rad(int(input("Solar Longitude (degrees): ")))
                if solar_long < np.deg2rad(0):
                    print('Error: Solar longitude must be a value between 0 and 360. Please try again.') # if solar longitude less than 0, return error
                elif solar_long > np.deg2rad(360):
                    print('Error: Solar longitude must be a value between 0 and 360. Please try again.') # if solar longitude less than 360, return error
                else:
                    valid = True
            except:
                print("Error: Solar longitude needs to be an integer between 0 and 360. Please try again.") # if solar longitude is not an integer, return error
    
        # error checker for top of atmosphere data input
        valid = False
        while not valid:
            try:
                ghi = input(str("GHI Data (.csv): "))
                ghi_data = csv_reader(ghi)
                valid = True
            except:
                print("Error: File not found. Please try again.") # if toa cannot be found as a csv file, return error
        
        # error checker for data formatting
        if not len(ghi_data) == len(z_rad) == len(op_data):
            print("Error: Data is not the same size. Please check files and try again.") # if files do not have the same number of rows, return error
        else:
            row = 0
            while row < len(ghi_data):
                if not len(ghi_data[row]) == len(z_rad[row]) == len(op_data[row]):
                    print("Error: Data is not the same size. Please check files and try again.") # if rows in each file do not have the same length, return error
                    break 
                else:
                    row += 1
                    valid2 = True
                    
    # calculates direct normal irradiance map    
    dni_irr = DNI_calc(solar_long, op_data, z_rad)

    # calculate diffuse horizontal irradiance map
    dhi_irr = DHI_calc(ghi_data, dni_irr, z_rad)

    i = 0
    ratio = []
    while i < len(dni_irr):
        row = []
        j = 0
        while j < len(dni_irr[i]):
            row.append(dni_irr[i][j]/dhi_irr[i][j])
            j += 1
        ratio.append(row)
        i += 1

    # sets axes ticks marks
    lat = [90, 86, 83, 79, 75, 71, 68, 64, 60, 56, 53, 49, 45, 41, 38, 34, 30, 26, 23, 19, 15, 11
           , 7, 4, 0, -4, -7, -11, -15, -19, -23, -26, -30, -34, -38, -41, -45, -49, -53, -56, -60
           , -64, -68, -71, -75, -79, -83, -86]
    long = [-180, -174, -162, -157, -151, -145, -140, -134, -128, -122, -117, -111, -105, -100, -94, -88
            , -82, -77, -71, -65, -60, -54, -48, -42, -37, -31, -25, -20, -14, -8, -2, 2, 8, 14, 20, 25
            , 31, 37, 42, 48, 54, 60, 65, 71, 77, 82, 88, 94, 100, 105, 111, 117, 122, 128, 134, 140, 145
            , 151, 157, 162, 174, 162, 174, 180]

    # intializes subplots
    fig,axes = plt.subplots(2, 2, figsize=(15, 10))

    # produces and formats heatmap for global horizontal irradiance data
    df_ghi = pd.DataFrame(ghi_irr, index = lat, columns = long)
    ghi_map = sns.heatmap(df_ghi, ax=axes[0,0], xticklabels=5, yticklabels=4, cbar_kws={'label': 'Irradiance (W/m^2)'})
    ghi_map.tick_params(axis='both', labelsize=8)
    ghi_map.set_title('Martian Global Horizontal Irradiance Map')
    ghi_map.set_ylabel('Latitude')
    ghi_map.set_xlabel('Longitude')
    
    # produces and formats heatmap for direct normal irradiance data
    df_dni = pd.DataFrame(dni_irr, index = lat, columns = long)
    dni_map = sns.heatmap(df_dni, ax=axes[0,1], xticklabels=5, yticklabels=4, cbar_kws={'label': 'Irradiance (W/m^2)'})
    dni_map.tick_params(axis='both', labelsize=8)
    dni_map.set_title('Martian Direct Normal Irradiance Map')
    dni_map.set_ylabel('Latitude')
    dni_map.set_xlabel('Longitude')

    # produces and formats heatmap for diffuse horizontal irradiance data
    df_dhi = pd.DataFrame(dhi_irr, index = lat, columns = long)
    dhi_map = sns.heatmap(df_dhi, ax=axes[1,0], xticklabels=5, yticklabels=4, cbar_kws={'label': 'Irradiance (W/m^2)'})
    dhi_map.tick_params(axis='both', labelsize=8)
    dhi_map.set_title('Martian Diffuse Horizontal Irradiance Map')
    dhi_map.set_ylabel('Latitude')
    dhi_map.set_xlabel('Longitude')

    # produces and formats map to display the ratio between diffuse and direct irradiane
    df_ratio = pd.DataFrame(ratio, index = lat, columns = long)
    dhi_map = sns.heatmap(df_ratio, ax=axes[1,0], xticklabels=5, yticklabels=4, cbar_kws={'label': 'DNI/DHI'})
    dhi_map.tick_params(axis='both', labelsize=8)
    dhi_map.set_title('Ratio of DNI and DHI Values')
    dhi_map.set_ylabel('Latitude')
    dhi_map.set_xlabel('Longitude')

    # displays the plots
    plt.tight_layout()
    plt.show()
    
    ### code for displaying individual data points ###

    # error checker for user input
    valid3 = False
    while valid3 == False:
        single_point = input("Would you to see data for a single point (y/n): ")

        if single_point == 'y':
            valid3 = True

            #asks user for coordinates and checks if they are valid
            valid = False
            while valid == False:
                x = input("Please select an x-coordinate (integer): ")
                try:
                    x = int(x)
                    if x < -180:
                        print("The x-coordinate must be a value between -180 and 180.")
                    elif x > 180:
                        print("The x-coordinate must be a value between -180 and 180.")
                    else:
                        valid = True
                except:
                    print("The x-coordinate must be an integer.") #if x cannot be set an int() variable, return error
            
            #same logic from x-coordinate applies to y-coordinate error checker
            valid = False
            while valid == False:
                y = input("Please select a y-coordinate (integer): ")
                try:
                    y = int(y)
                    if y < -90:
                        print("The y-coordinate must be a value between -90 and 90.")
                    elif y > 90:
                        print("The y-coordinat must be a value between -90 and 90.")
                    else:
                        valid = True
                except:
                    print("The y-coordinate must be an integer.") #if y cannot be set an int() variable, return error

        # ends the program if user doesn't want to choose a data point
        elif single_point == 'n':
            print("Thank you for using this program!")
            exit()
        
        # error message if user doesn't select y or n
        else:
            print("Please type a letter 'y' for yes and 'n' for no.")
    
    # finds the closest value to the x-coord the user selected
    j = 0
    while j < len(long):
        if x == long[j]:
            x_sel = long[j]
            break
        elif x > long[j]:
            j += 1
            continue
        elif x < long[j]: #iterates through the array until it find a value less than the selected value 
            if abs(x-long[j]) > abs(x-long[j-1]): #checks if it is closer to upper bound or lower bound
                x_sel = long[j-1]
                j = j-1
                break
            else:
                x_sel = long[j]
                break
    
    # finds the closest value to the y-coord the user selected
    l = 0
    while l < len(lat):
        if y == lat[l]:
            y_sel = lat[l]
            break
        elif y < lat[l]:
            l += 1
            continue
        elif y > lat[l]: #iterates through the array until it find a value less than the selected value (lat is ordered from greatest to least)
            if abs(y-lat[l]) > abs(y-lat[l-1]): #checks if it is closer to the upper bound or lower bound
                y_sel = lat[l-1]
                l = l-1
                break
            else:
                y_sel = lat[l]
                break

    # find the closest ghi dni and dhi data points
    ghi_sel = round(ghi_data[l][j], 4)
    dni_sel = round(dni_irr[l][j], 4)
    dhi_sel = round(dhi_irr[l][j], 4)

    # prints values with formatting
    print(f"The Global Horizontal Irradiance value nearest to the coordinates ({x},{y}) is roughly {ghi_sel} W/m^2.")
    print(f"The Direct Normal Irradiance value nearest to the coordinates ({x},{y}) is roughly {dni_sel} W/m^2.")
    print(f"The Diffuse Horizontal Irradiance value nearest to the coordinates({x},{y}) is roughly {dhi_sel} W/m^2.")
        

if __name__ == "__main__":
    main()
