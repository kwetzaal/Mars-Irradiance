function surf_irr = dniCalculations(solar_long, optical_depth, zenith_ang)
    %% Initialize constants %%
    mean_irr = 588.6;  % Mean solar irradiance
    eccentricity = 0.0934;
    Ls_p = 251;  % Convert degrees to radians

    %% Calculate Top of Atmosphere (TOA) irradiance %%
    toa = mean_irr * ((1 + (eccentricity * cosd(solar_long - Ls_p)) / (1 - eccentricity^2))^2);

    %% Calculate DNI %%

    % calculate cos(zenith_ang)
    sz_1 = size(zenith_ang.SolarZenithAngle);
    zenithAngDouble = zeros(sz_1(1), sz_1(2), sz_1(3));
    for i = 1:sz_1(1)
        for j = 1:sz_1(2)
            for k = 1:sz_1(3)
                if zenith_ang.SolarZenithAngle{i,j,k} < 0         
                    zenith_ang.SolarZenithAngle{i,j,k} = 0;
                end
                zen = str2double(zenith_ang.SolarZenithAngle{i,j,k});
                cosZenith = cosd(zen);
                zenithAngDouble(i,j,k) = cosZenith;
            end
        end
    end
    
    % calculate exp(-optical_depth)
    sz_2 = size(optical_depth.DailyMeanDustColumnVisibleOpticalDepthAboveSurface);
    opticalDepthDouble = zeros(sz_2(1), sz_2(2), sz_2(3));
    for l = 1:sz_2(1)
        for m = 1:sz_2(2)
            for n = 1:sz_2(3)
                expOpticalDepth = exp(str2double(optical_depth.DailyMeanDustColumnVisibleOpticalDepthAboveSurface{l,m,n}));
                opticalDepthDouble(l,m,n) = expOpticalDepth;
            end
        end
    end
    
    % calculates DNI 
    surf_irr = round(toa * zenithAngDouble .* opticalDepthDouble, 6);
end

%% INITIALIZE DATA %%

% Optical Depth
folder = 'C:\Users\kiraz\OneDrive\Documents\School\Purdue Freshman\VIP ABC-PV\Mars Irradiance(Matlab)\DailyMeanDustColumnVisibleOpticalDepthAboveSurface\'; % opens selected folder (Optical Depth)
files = dir(fullfile(folder, '*.mat'));  % List all .mat files

opticalDepthData = [];

% loops through all .mat files in the folder
for k = 1:length(files)
    filepath = fullfile(folder, files(k).name);
    if ~exist(filepath, 'file')
        message = printf('%s does not exist', filepath);
    else
        fileData = load(filepath)'; % load .mat file
        opticalDepthData = cat(4, opticalDepthData, fileData); % concatonates to 4th Dimension of struct (time, lat, long, solar long)
    end 
end

% Zenith Angle
folder = 'C:\Users\kiraz\OneDrive\Documents\School\Purdue Freshman\VIP ABC-PV\Mars Irradiance(Matlab)\SolarZenithAngle\'; % opens selected folder (Zenith Angle)
files = dir(fullfile(folder, '*.mat'));  % List all .mat files

solarZenithData = [];

% loops through all .mat files in the folder
for k = 1:length(files)
    filepath = fullfile(folder, files(k).name);
    if ~exist(filepath, 'file')
        message = printf('%s does not exist', filepath);
    else
        fileData = load(filepath)'; % load .mat file
        solarZenithData = cat(4, solarZenithData, fileData); % concatonates to 4th Dimension of struct (time, lat, long, solar long)
    end 
end

% Solar Longitude
solarLongitudeData = 15;30;360;

%% CALCULATIONS %%

dniData = [];
i = 1;
while i <= length(solarLongitudeData)
    dniDataForSolarLong = dniCalculations(solarLongitudeData(i), opticalDepthData{ : , : , : , i}, solarZenithData{ : , : , :, i});
    dniData = cat(4, dniData, dniDataForSolarLong);
    i = i + 1;
end

%save('DNI_Data','dniData')
