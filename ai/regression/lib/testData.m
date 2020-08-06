function y_test = testData(X, y, theta, mixer)

% ============================================================================
% This function test the accuracy of the regression.

% Input :
%           - X : input matrix (normalized)
%           - y_test : target vector obtained by regression
%           - theta : parameters obtained by the gradient descent algorithm
%           - mixer : vector of mixers to test

% Output :
%           - y : vector of predicitons

% ----------------------------------------------------
% Author : Valérie Bibeau, Polytechnique Montréal, 2020
% ============================================================================

y_test = X(mixer,:) * theta;

figure;
plot(mixer, y_test, 'o')
hold on
plot(mixer, y(mixer), '*')
legend('Target from regression', 'Target from data')