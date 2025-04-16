function dhi = DHI_Calculations(ghi_data, dni_data, zenith_ang)
    %% Calculate DHI %%

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
    
    dniDouble = str2double(dni_data);
    ghiDouble = str2double(ghi_data);
    
    dhi = double((ghiDouble-dniDouble).*zenithAngDouble);
end
%% INITIALIZE DATA %%

% Global Horizontal Irradiance 
folder = 'C:\Users\kiraz\OneDrive\Documents\School\Purdue Freshman\VIP ABC-PV\Mars Irradiance(Matlab)\InciddentSolarFluxOnHorizontalSurface\'; % opens selected folder (Optical Depth)
files = dir(fullfile(folder, '*.mat'));  % List all .mat files

ghiData = [];

% loops through all .mat files in the folder
for k = 1:length(files)
    filepath = fullfile(folder, files(k).name);
    if ~exist(filepath, 'file')
        message = printf('%s does not exist', filepath);
    else
        fileData = load(filepath)'; % load .mat file
        ghiData = cat(4, ghiData, fileData); % concatonates to 4th Dimension of struct (time, lat, long, solar long)
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

% Direct Normal Irradiance
dniData = load('DNI_Data.mat')';


%% CALCULATIONS %%
dhiData = [];
i = 1;
while i <= length(solarLongitudeData)
    dhiDataCalc = DHI_Calculations(ghiData( :, :, :, i), dniData( : , : , : , i), solarZenithData( : , : , :, i));
    dhiData = cat(4, dhiData, dhiDataCalc);
    i = i + 1;
end
disp(dhiData)
%save('DHI_Data','dhiData')
