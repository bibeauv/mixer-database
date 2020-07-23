function [jVal, gradient] = costFunctionReg(X, y, theta, alpha, lambda)

% ============================================================================
% This function calculate the cost function J
% and its gradient for each parameters theta

% Input :
%           - X : input matrix
%           - y : target vector
%           - theta : initial theta
%           - alpha : learning rate
%           - lambda : regularization constant

% Output :
%           - jVal : value of J
%           - gradient : gradient of J for each theta

% ----------------------------------------------------
% Autor : Valérie Bibeau, Polytechnique Montréal, 2020
% ============================================================================

m = length(y);

[jVal, gradient] = costFunction(X, y, theta, alpha);

jVal = jVal + lambda/(2*m) * sum(theta(2:end).^2);
gradient(2:end) = gradient(2:end) + lambda*alpha/m * theta(2:end);
