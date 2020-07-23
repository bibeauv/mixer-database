function [J_history, theta] = gradientDescent(X, y, theta, alpha, max_iters, regularization, lambda)

% ============================================================================
% This function calculate the parameters theta 
% of a regression problem with the gradient descent algorithm

% Input :
%           - X : input matrix
%           - y : target vector
%           - theta : initial theta
%           - alpha : learning rate
%           - max_iters : maximum of iterations allowed
%           - regularization : if the regularization term are added or no
%           - lambda : regularization constant

% Output :
%           - J_history : history of the value of J
%           - theta : final theta

% ----------------------------------------------------
% Autor : Valérie Bibeau, Polytechnique Montréal, 2020
% ============================================================================

J_history = [];
diff = 1;
it = 0;

while it < max_iters
    if regularization == true
        [jVal, gradient] = costFunctionReg(X, y, theta, alpha, lambda);
    else
        [jVal, gradient] = costFunction(X, y, theta, alpha);
    end

    J_history = [J_history; jVal];

    theta = theta - gradient;

    fprintf('Nb of iteration: %d \n', it)
    fprintf('Value of J(theta): %e \n', jVal)
    if it > 0
        diff = abs(J_history(it+1) - J_history(it));
        fprintf('Difference: %e \n', diff);
    end

    plot(1:it+1, J_history(1:it+1))
    shg; pause(0.01);

    it = it + 1;
end
