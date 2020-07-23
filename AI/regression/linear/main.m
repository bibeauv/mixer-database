clc; clear all;

% ============================================================================
% This main programm will be able to train the mixer database.
% This programm is to test the regression algorithm.

% First, the programm will train the mixer dataset by gradient descent.
% Second, the programm will calculate the parameters with the normal equation.

% ----------------------------------------------------
% Autor : Valérie Bibeau, Polytechnique Montréal, 2020
% ============================================================================

% Order of the features
% T_D       : 2
% H_T       : 3
% T_C       : 4
% D_W       : 5
% D_WHub    : 6
% E         : 7
% theta     : 8
% omega     : 9
% density   : 10
% viscosity : 11
% Re        : 12

% Get the database
[X, y] = getMixerData('mixer_database_1-6250.txt');

% Remove feature that are includ in Reynolds number
remove = [7 8 9 10 11];
X(:,remove) = [];

% Remove outlier data (Re that are too low, therefor Np that are too high)
clean = [7];
[X, y] = cleanUp(X, y, clean, 0.1);

% Feature scaling
no_scaling = [1];
X_norm = featureScaling(X, no_scaling);

% Gradient descent without regularization
n = size(X,2);
theta = zeros(n,1);
alpha = 0.1;
max_iters = 200;
lambda = 10000;
[J_history, theta] = gradientDescent(X_norm, y, theta, alpha, max_iters, true, lambda);

% Prediction
X_predict = [1, ...         
             3.0, ...       % T/D
             1.4, ...       % H/T
             2.2, ...       % T/C
             3.5, ...       % D/W
             2.1, ...       % D/W_Hub
             2.6526];       % Re

X_predict_norm = predictScaling(X, X_predict, no_scaling);

y_predict = X_predict_norm*theta;

fprintf('Prediction for the power number: %.2f \n', y_predict)
disp('Power number from simulation: 21.729078')