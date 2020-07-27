function [X_clean, y_clean] = cleanUp(X, y, feature, limit)

% ============================================================================
% This function cleans up the outliers.

% Input :
%           - X : input matrix
%           - y : target vector
%           - feature : j of theta_j that will be removed from the features
%           - limit : outliers

% Output :
%           - X_clean : new input matrix
%           - y_clean : new target vector

% ----------------------------------------------------
% Author : Valérie Bibeau, Polytechnique Montréal, 2020
% ============================================================================

m = size(X,1);

X_clean = X;
y_clean = y;

pos = [];
for f = 1:length(feature)
    for i = 1:m
        if X_clean(i,feature(f)) < limit
            pos = [pos, i];
        end
    end
end

X_clean(pos,:) = [];
y_clean(pos) = [];