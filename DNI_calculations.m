function surf_irr_and_time = DNI_calc_time(solar_long, optical_depth, zenith_ang)
    % Initialize constants
    mean_irr = 588.6;  % Mean solar irradiance
    eccentricity = 0.0934;
    Ls_p = 251;  % Convert degrees to radians

    % Calculate Top of Atmosphere (TOA) irradiance
    toa = mean_irr * ((1 + (eccentricity * cosd(solar_long - Ls_p)) / (1 - eccentricity^2))^2);

    % Extract time, optical depth, and zenith angle
    time = optical_depth(:, 1).';  % Time values
    tau = optical_depth(:, 2).';   % Optical depth values
    zenith = zenith_ang(:, 2).';   % Zenith angles

    % Calculate surface irradiance
    surf_irr = double(round(toa.*cosd(zenith).*exp(-tau), 6));
    
    % Store results in a cell array
    surf_irr_and_time = {time, surf_irr};
end

od_name = input("Optical Depth Data (.csv): ");
od_data = readmatrix(od_name);

za_name = input("Zenith Angle Data (.csv): ");
za_data = readmatrix(za_name);
za_data(za_data > 90) = 90;

ls = double(input("Solar Longitude (deg and int): "));

dni_and_time = DNI_calc_time(ls_rad, od_data, za_data);

dni = dni_and_time{1, 2};
time = dni_and_time{1, 1};

plot(time, dni)
xlabel('Time')
ylabel('Direct Normal Irradiance (W/m^2)')
title('DNI vs. Time')

writecell(dni_and_time.', 'time_0_DNI.csv')
