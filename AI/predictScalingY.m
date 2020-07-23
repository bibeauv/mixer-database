function y_predict = predictScalingX(y, y_norm, no_scaling)

% ============================================================================
% This function transform the normalized output y to the real value

% Input :
%           - y : target vector
%           - y_norm : prediction normalized
%           - no_scaling : j of theta_j that doesn't need scaling

% Output :
%           - y_predict : real value of output

% ----------------------------------------------------
% Autor : Valérie Bibeau, Polytechnique Montréal, 2020
% ============================================================================

max_y = max(y); min_y = min(y); 
u_y = mean(y);
s_y = max_y - min_y;

y_predict = y_norm*s_y+u_y;