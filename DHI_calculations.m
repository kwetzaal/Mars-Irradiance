function dhi = DHI_Calculations(ghi_data, dni_data, zenith_ang)
    %% Calculate DHI %%

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

    % calculate cos(zenith_ang)
    sz_2 = size(ghi_data);
    ghiDouble = zeros(sz_2(1), sz_2(2), sz_2(3));
    dniDouble = zeros(sz_2(1), sz_2(2), sz_2(3));
    for l = 1:sz_2(1)
        for m = 1:sz_2(2)
            for n = 1:sz_2(3)
                ghiDouble(l,m,n) = str2double(ghi_data(l,m,n));
                dniDouble(l,m,n) = dni_data(l,m,n);
            end
        end
    end

    dhi_results = (ghiDouble-dniDouble).*zenithAngDouble;
    dhi = reshape(dhi_results, 25, 64, 48, 1);
end

%% INITIALIZE DATA %%

% Global Horizontal Irradiance 
folder = 'C:\Users\kiraz\OneDrive\Documents\School\Purdue Freshman\VIP ABC-PV\Mars Irradiance(Matlab)\IncidentSolarFluxOnHorizontalSurface\'; % opens selected folder (Optical Depth)
files = dir(fullfile(folder, '*.mat'));  % List all .mat files

ghiData = cell(25, 64, 48, 0); % empty 4D array with the size you want 

% loops through all .mat files in the folder
for k = 1:length(files)
    filepath = fullfile(folder, files(k).name);
    if ~exist(filepath, 'file')
        message = printf('%s does not exist', filepath);
    else
        fileData = load(filepath)'; % load .mat file
        sz = size(fileData.IncidentSolarFluxOnHorizontalSurface);
        fileData4D = reshape(fileData.IncidentSolarFluxOnHorizontalSurface, sz(1), sz(2), sz(3), 1); % turns data into 4D array
        ghiData = cat(4, ghiData, fileData.IncidentSolarFluxOnHorizontalSurface); % concatonates to 4th Dimension of struct (time, lat, long, solar long)
    end 
end

% Zenith Angle
folder = 'C:\Users\kiraz\OneDrive\Documents\School\Purdue Freshman\VIP ABC-PV\Mars Irradiance(Matlab)\SolarZenithAngle\'; % opens selected folder (Zenith Angle)
files = dir(fullfile(folder, '*.mat'));  % List all .mat files

solarZenithData = cell(25, 64, 48, 0); % empty 4D array with the size you want 

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

% Direct Normal Irradiance
dniData = load('DNI_Data.mat')';

%solarlongitude for looping
solarLongitudeData = 15:30:360;

%% CALCULATIONS %%
dhiData = [];
i = 1;
while i <= length(solarLongitudeData)
    dhiDataCalc = DHI_Calculations(ghiData( :, :, :, i), dniData.dniData( : , : , : , i), solarZenithData( : , : , :, i));
    dhiData = cat(4, dhiData, dhiDataCalc);
    i = i + 1;
end

save('DHI_Data','dhiData')
