function dhi_and_time = DHI_calc_time(ghi_data, dni_data, zenith_ang)
    % Extract time, optical depth, and zenith angle
    time = ghi_data(:, 1).';  % Time values
    ghi = ghi_data(:, 2).';   % Global Horizontal Irradiance values
    dni = dni_data(2, :);   % Direct Normal Irradiance values
    zenith = zenith_ang(:,2).'; % Zenith angles values
    disp(dni)

    % Calculate surface irradiance
    dhi = double((ghi-dni).*cosd(zenith));

    % Store results in a cell array
    dhi_and_time = {double(time), dhi};
    disp(dhi_and_time)
end

ghi_name = input("Global Horizontal Irradiance Data (.csv): ");
ghi_data = readmatrix(ghi_name);

dni_name = input("Direct Normal Irradiance Data (.csv): ");
dni_data = readmatrix(dni_name);

za_name = input("Zenith Angle Data (.csv): ");
za_data = readmatrix(za_name);
za_data(za_data > 90) = 90;

dhi_data = DHI_calc_time(ghi_data, dni_data, za_data);

dhi = dhi_data{:, 2};
time = dhi_data{:, 1};

plot(time, dhi)
xlabel('Time')
ylabel('Diffuse Horizontal Irradiance (W/m^2)')
title('DHI vs. Time')