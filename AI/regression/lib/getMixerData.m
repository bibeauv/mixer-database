function [X, y] = getMixerData(fileName)

% ============================================================================
% This function gets the data of the mixers.

% Input :
%           - fileName : name of the text file where the database of the
%                        mixers are

% Output :
%           - X : input matrix
%           - y : target vector

% ----------------------------------------------------
% Author : Valérie Bibeau, Polytechnique Montréal, 2020
% ============================================================================

mixer = {};
T_D = [];
H_T = [];
T_C = [];
D_W = [];
D_WHub = [];
E = [];
theta = [];
omega = [];
density = [];
viscosity = [];
Re = [];
Np = [];

disp('Reading data file ...')
fic_data = fopen(fileName,'r');
if fic_data == -1
    disp('Error: The datafile did not open correctly.')
else
    mixer{end+1} = fscanf(fic_data,'%s',1);
    while isempty(mixer{end}) == 0
        fscanf(fic_data,'%s',1); T_D(end+1) = fscanf(fic_data,'%f',1);
        fscanf(fic_data,'%s',1); H_T(end+1) = fscanf(fic_data,'%f',1);
        fscanf(fic_data,'%s',1); T_C(end+1) = fscanf(fic_data,'%f',1);
        fscanf(fic_data,'%s',1); D_W(end+1) = fscanf(fic_data,'%f',1);
        fscanf(fic_data,'%s',1); D_WHub(end+1) = fscanf(fic_data,'%f',1);
        fscanf(fic_data,'%s',1); E(end+1) = fscanf(fic_data,'%f',1);
        fscanf(fic_data,'%s',1); theta(end+1) = fscanf(fic_data,'%f',1);
        fscanf(fic_data,'%s',1); omega(end+1) = fscanf(fic_data,'%f',1);
                                 density(end+1) = 1;
                                 viscosity(end+1) = 1;
        fscanf(fic_data,'%s',1); Re(end+1) = fscanf(fic_data,'%f',1);
        fscanf(fic_data,'%s',1); Np(end+1) = fscanf(fic_data,'%f',1);

        mixer{end+1} = fscanf(fic_data,'%s',1);
    end
end
fclose(fic_data);
disp('Done reading datafile!')

% Create the X matrix and the y vector
m = length(mixer)-1;
X = [ones(m,1), ...
    T_D', ...
    H_T', ...
    T_C', ...
    D_W', ...
    D_WHub', ...
    E', ...
    theta', ...
    omega', ...
    density', ...
    viscosity', ...
    Re'];
y = Np';