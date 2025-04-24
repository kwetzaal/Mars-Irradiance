function dni = dniCalculations(solar_long, optical_depth, zenith_ang)
    %% Initialize constants %%
    mean_irr = 588.6;  % Mean solar irradiance
    eccentricity = 0.0934;
    Ls_p = 251;  % Convert degrees to radians

    %% Calculate Top of Atmosphere (TOA) irradiance %%
    toa = mean_irr * ((1 + (eccentricity * cosd(solar_long - Ls_p)) / (1 - eccentricity^2))^2);

    %% Calculate DNI %%

    % calculate cos(zenith_ang)
    sz_1 = size(zenith_ang);
    zenithAngDouble = zeros(sz_1(1), sz_1(2), sz_1(3));
    for i = 1:sz_1(1)
        for j = 1:sz_1(2)
            for k = 1:sz_1(3)
                zen = str2double(zenith_ang{i,j,k});
                if zen > 90         
                    zen = 90;
                end
                if zen < 0         
                    zen = 0;
                end
                cosZenith = cosd(zen);
                zenithAngDouble(i,j,k) = cosZenith;
            end
        end
    end
    
    % calculate exp(-optical_depth)
    sz_2 = size(optical_depth);
    opticalDepthDouble = zeros(sz_2(1), sz_2(2), sz_2(3));
    for l = 1:sz_2(1)
        for m = 1:sz_2(2)
            for n = 1:sz_2(3)
                expOpticalDepth = exp(str2double(optical_depth{l,m,n}));
                opticalDepthDouble(l,m,n) = expOpticalDepth;
            end
        end
    end
    
    % calculates DNI 
    surf_irr = round(toa .* zenithAngDouble .* opticalDepthDouble, 6);
    dni = reshape(surf_irr, 25, 64, 48, 1);
end

%% INITIALIZE DATA %%

% Optical Depth
folder = 'C:\Users\kiraz\OneDrive\Documents\School\Purdue Freshman\VIP ABC-PV\Mars Irradiance(Matlab)\DailyMeanDustColumnVisibleOpticalDepthAboveSurface\'; % opens selected folder (Optical Depth)
files = dir(fullfile(folder, '*.mat'));  % List all .mat files

opticalDepthData = cell(25, 64, 48, 0);

% loops through all .mat files in the folder
for k = 1:length(files)
    filepath = fullfile(folder, files(k).name);
    if ~exist(filepath, 'file')
        message = printf('%s does not exist', filepath);
    else
        fileData = load(filepath)'; % load .mat file
        sz = size(fileData.DailyMeanDustColumnVisibleOpticalDepthAboveSurface);
        fileData4D = reshape(fileData.DailyMeanDustColumnVisibleOpticalDepthAboveSurface, sz(1), sz(2), sz(3), 1); % turns data into 4D array
        opticalDepthData = cat(4, opticalDepthData, fileData.DailyMeanDustColumnVisibleOpticalDepthAboveSurface); % concatonates to 4th Dimension of struct (time, lat, long, solar long)
    end 
end

% Zenith Angle
folder = 'C:\Users\kiraz\OneDrive\Documents\School\Purdue Freshman\VIP ABC-PV\Mars Irradiance(Matlab)\SolarZenithAngle\'; % opens selected folder (Zenith Angle)
files = dir(fullfile(folder, '*.mat'));  % List all .mat files

solarZenithData = cell(25, 64, 48, 0);

% loops through all .mat files in the folder
for k = 1:length(files)
    filepath = fullfile(folder, files(k).name);
    if ~exist(filepath, 'file')
        message = printf('%s does not exist', filepath);
    else
        fileData = load(filepath)'; % load .mat file
        sz = size(fileData.SolarZenithAngle);
        fileData4D = reshape(fileData.SolarZenithAngle, sz(1), sz(2), sz(3), 1); % turns data into 4D array
        solarZenithData = cat(4, solarZenithData, fileData.SolarZenithAngle); % concatonates to 4th Dimension of struct (time, lat, long, solar long)
    end 
end

% Solar Longitude
solarLongitudeData = 15:30:360;
disp(solarLongitudeData)

%% CALCULATIONS %%

dniData = zeros(25, 64, 48, 0);
i = 1;
while i <= length(solarLongitudeData)
    dniDataForSolarLong = dniCalculations(solarLongitudeData(i), opticalDepthData( : , : , : , i), solarZenithData( : , : , :, i));
    disp(size(dniDataForSolarLong))
    dniData = cat(4, dniData, dniDataForSolarLong);
    i = i + 1;
end
disp(dniData)

save('DNI_Data','dniData')
