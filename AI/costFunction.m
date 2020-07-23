function [jVal, gradient] = costFunction(X, y, theta, alpha)

% ============================================================================
% This function calculate the cost function J
% and its gradient for each parameters theta

% Input :
%           - X : input matrix
%           - y : target vector
%           - theta : initial theta
%           - alpha : learning rate

% Output :
%           - jVal : value of J
%           - gradient : gradient of J for each theta

% ----------------------------------------------------
% Autor : Valérie Bibeau, Polytechnique Montréal, 2020
% ============================================================================

m = length(y);

sum_j = 0;
sum_dj = zeros(length(theta),1);
for i = 1:m
    sum_j = sum_j + (X(i,:)*theta - y(i))^2;
    for t = 1:length(theta)
        sum_dj(t) = sum_dj(t) + (X(i,:)*theta - y(i))*X(i,t);
    end
end

jVal = sum_j/(2*m);
gradient = sum_dj*alpha/m;
