function X_norm = predictScaling(X, X_predict, no_scaling)

% ============================================================================
% This function scales the features X and the prediction y

% Input :
%           - X : input matrix
%           - X_predict : input features for prediction
%           - no_scaling : j of theta_j that doesn't need scaling

% Output :
%           - X_norm : input matrix normalized

% ----------------------------------------------------
% Autor : Valérie Bibeau, Polytechnique Montréal, 2020
% ============================================================================

n = size(X,2);

X_norm = X_predict;

for f = 1:n
    if all(f ~= no_scaling)
        maximum = max(X(:,f));
        minimum = min(X(:,f));
        u = mean(X(:,f));
        s = maximum - minimum;
        X_norm(1,f) = (X_predict(1,f) - u)/s;
    end
end