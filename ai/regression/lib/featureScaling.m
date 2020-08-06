function X_norm = featureScaling(X, no_scaling)

% ============================================================================
% This function scales the matrix X and the target vector y.

% Input :
%           - X : input matrix
%           - y : target vector
%           - no_scaling : j of theta_j that doesn't need scaling

% Output :
%           - X_norm : input matrix normalized
%           - y_norm : target vector normalized

% ----------------------------------------------------
% Author : Valérie Bibeau, Polytechnique Montréal, 2020
% ============================================================================

n = size(X,2);
m = size(X,1);

X_norm = X;

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