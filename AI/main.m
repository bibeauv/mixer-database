clc; clear all;

% ============================================================================
% This main programm will be able to train the mixer database.
% This programm is to test the regression algorithm.

% First, the programm will train the mixer dataset by gradient descent.
% Second, the programm will calculate the parameters with the normal equation.

% ----------------------------------------------------
% Autor : Valérie Bibeau, Polytechnique Montréal, 2020
% ============================================================================

% Get the database
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
fic_data = fopen('mixer_database_1-6250.txt','r');
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
n = 10;
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
    viscosity'];
y = Np';

% Feature scaling
no_scaling = [7, 8, 10, 11];
[X_norm, y_norm] = featureScaling(X, y, no_scaling);

% Gradient descent without regularization
theta = zeros(n+1,1);
alpha = 0.1;
max_iters = 1500;
lambda = 1000;
tol = 1e-10;
[J_history, theta] = gradientDescent(X_norm, y_norm, theta, alpha, tol, max_iters, true, lambda);

% Predict
X_predict = [1, ...         
             3.0, ...       % T/D
             1.4, ...       % H/T
             2.2, ...       % T/C
             3.5, ...       % D/W
             2.1, ...       % D/W_Hub
             0.1, ...       % E
             0.785398, ...  % theta
             150, ...       % omega
             1, 1];         % density, viscosity

X_predict_norm = predictScalingX(X, X_predict, no_scaling);

y_predict_norm = X_predict_norm*theta;

y_predict = predictScalingY(y, y_predict_norm, no_scaling);

fprintf('Prediction for the power number: %.2f \n', y_predict)
disp('Power number from simulation: 643.824543')