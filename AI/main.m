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
[X, y] = getMixerData('mixer_database_1-6250.txt');

% Feature scaling
no_scaling = [1, 7, 8, 10, 11];
X_norm = featureScaling(X, no_scaling);

% Gradient descent without regularization
n = size(X,2);
theta = zeros(n,1);
alpha = 0.1;
max_iters = 1000;
lambda = 1000;
tol = 1e-10;
[J_history, theta] = gradientDescent(X_norm, y, theta, alpha, max_iters, false, lambda);

% Prediction
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

X_predict_norm = predictScaling(X, X_predict, no_scaling);

y_predict = X_predict_norm*theta;

fprintf('Prediction for the power number: %.2f \n', y_predict)
disp('Power number from simulation: 643.824543')