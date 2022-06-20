import MixerNN as MNN
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow import keras
from sklearn.model_selection import GridSearchCV

# =================================================================================
# Main program to do a grid search on the hyperparameters

# Author: Valérie Bibeau, Polytechnique Montréal, 2022
# =================================================================================

# Read the data
data = MNN.read_mixerdata('mixer_database_0-19999.txt',19)

# Clean the data
data = MNN.clean_low_Re(data, 0.1, False)

# Set the features and the target values for the training and testing set
target_index = [0, 1, 2, 3, 5, 6, 7]
X_train, X_test, y_train, y_test, scaler_X, scaler_y = MNN.initial_setup(data, 0.3, target_index, 8, 42)

# Grid search
def create_model(neurons=1, layers=1, activation='tanh', optimizer='adam'):
    model = Sequential()
    layer = 0
    while layer < layers:
        model.add(Dense(neurons, input_dim=7, kernel_initializer=keras.initializers.GlorotUniform(), activation=activation))
        layer += 1
    model.add(Dense(1, kernel_initializer=keras.initializers.GlorotUniform(), activation='linear'))
    model.compile(loss='mse', optimizer=optimizer, metrics=['mse'])
    return model

seed = 7
np.random.seed(seed)
model = keras.wrappers.scikit_learn.KerasRegressor(build_fn=create_model, epochs=1000, verbose=0)
optimizer = ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
activation = ['relu','tanh']
batch_size = [10,50,100,200,500]
neurons = [4,8,16,24,32,40]
layers = [2,3,4,5,6]
param_grid = dict(optimizer=optimizer,
                  activation=activation,
                  batch_size=batch_size,
                  neurons=neurons,
                  layers=layers)
grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, cv=3, scoring='neg_mean_squared_error')
grid_result = grid.fit(X_train, y_train)
# Summarize results
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))