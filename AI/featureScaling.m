function [X_norm, y_norm] = featureScaling(X, y, no_scaling)

% ============================================================================
% This function scales the matrix X and the target vector y

% Input :
%           - X : input matrix
%           - y : target vector
%           - no_scaling : j of theta_j that doesn't need scaling

% Output :
%           - X_norm : input matrix normalized
%           - y_norm : target vector normalized

% ----------------------------------------------------
% Autor : Valérie Bibeau, Polytechnique Montréal, 2020
% ============================================================================

n = size(X,2);
m = size(X,1);

X_norm = X;
y_norm = y;

% Scaling of the features
for f = 2:n
    if all(f ~= no_scaling)
        maximum = max(X(:,f));
        minimum = min(X(:,f));
        u = mean(X(:,f));
        s = maximum - minimum;
        for i = 1:m
            X_norm(i,f) = (X(i,f) - u)/s;
        end
    end
end

% Scaling of the target
max_y = max(y); min_y = min(y); 
u_y = mean(y);
s_y = max_y - min_y;
for k = 1:m
    y_norm(k) = (y(k) - u_y)/s_y;
end