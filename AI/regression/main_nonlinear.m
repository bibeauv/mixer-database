clc; clear all;

path = pwd;
addpath([pwd, '/lib'])

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

% Non-linear features
n = size(X,2);
for i = 2:n
    X(:,end+1) = X(:,i).^2;
    if i ~= 7
        X(:,end+1) = X(:,i).*X(:,7);
    end
end
n = size(X,2);

% Feature scaling
no_scaling = [1];
X_norm = featureScaling(X, no_scaling);

% Gradient descent without regularization
theta = zeros(n,1);
alpha = 0.1;
max_iters = 1500;
lambda = 10;
[J_history, theta] = gradientDescent(X_norm, y, theta, alpha, lambda, max_iters);

% Test data
y_test = testData(X_norm, y, theta, [505:514]);