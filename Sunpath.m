function sunpath_calcs = sunpath(Ls, time, lat)
    solar_alt = zeros(size(time));
    solar_azi = zeros(size(time));
    
    declination = asin(0.42565 * sin(Ls)) + 0.25 * sind(Ls); % From JPL
    for i = 1:length(time)
        hour_angle = deg2rad(15 * (12 - time(i))); % time in Martian hour (1/24 sol)
        
        % From Earth models
        solar_alt(i) = rad2deg(asin(sin(lat) * sin(declination) + cos(lat) * cos(declination) * cos(hour_angle)));
        solar_azi(i) = -rad2deg(asin(cos(declination) * sin(hour_angle) / cosd(solar_alt(i))));
    end

    sunpath_calcs = {solar_alt, solar_azi};
end

od_name = input("Optical Depth Data (.csv): ");
od_data = readmatrix(od_name);
time = od_data(:, 1);

lat = double(input("Latitude: "));

ls = double(input("Solar Longitude (deg and int): "));
ls_rad = deg2rad(ls);

sunpath_calcs = sunpath(ls_rad, time, lat);

solar_alt = sunpath_calcs{:, 1};
solar_azi = sunpath_calcs{:, 2};

plot(solar_azi, solar_alt)
xlabel('Solar Azimuth')
ylabel('Solar Altitude')
title('Sun Path')