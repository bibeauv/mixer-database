import MixerNN as MNN
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import pandas

# =================================================================================
# Main program to find and build the model that has a better performance

# Author: Valérie Bibeau, Polytechnique Montréal, 2020
# =================================================================================

# Read the data
data = MNN.read_mixerdata('mixer_database_0-19999.txt',19)

# Clean the data
data = MNN.clean_low_Re(data, 0.1, False)

# Set the features and the target values for the training and testing set
target_index = [0, 1, 2, 3, 5, 6, 7]
X_train, X_test, y_train, y_test, scaler_X, scaler_y = MNN.initial_setup(data, 0.3, target_index, 8, 42)

# Try different model
no_params = []
val_mse = []
val_mae = []
val_mape = []
hist_a = []
hist_l = []
hist_u = []
hist_lambda = []
mse = []
for a in np.array(['deep']):
    for l in np.array([2,3,4,5]):
        for u in np.array([6,12,18,24]):
            for Lambda in np.array([1e-10]):
              history, model, params = MNN.fit_model( X_train=X_train, y_train=y_train,
                                                      no_features=len(target_index),
                                                      learning_rate=0.1,
                                                      l2=Lambda,
                                                      epochs=1000,
                                                      val_frac=0.2,
                                                      architecture=a,
                                                      units=u,
                                                      layers=l,
                                                      activation='tanh',
                                                      verbose=0 )
              
              # Trace the history
              hist_a.insert(len(hist_a), a)
              hist_l.insert(len(hist_l), l)
              hist_u.insert(len(hist_u), u)
              hist_lambda.insert(len(hist_lambda), Lambda)
              mse.insert(len(mse), history.history['mse'][-1])

              # Gather the number of parameters
              no_params.insert(len(no_params), params)

              # Gather the metrics for each NN
              val_mse.insert(len(val_mse), history.history['val_mse'][-1])
              val_mae.insert(len(val_mae), history.history['val_mae'][-1])
              val_mape.insert(len(val_mape), history.history['val_mape'][-1])

mse_best_pos = np.argmin(val_mse)
print("Best model based on MSE is with %s architecture, %d units and %d layers (%d parameters)" 
       % (hist_a[mse_best_pos], hist_u[mse_best_pos], hist_l[mse_best_pos], no_params[mse_best_pos]))
mae_best_pos = np.argmin(val_mae)
print("Best model based on MAE is with %s architecture, %d units and %d layers (%d parameters)" 
       % (hist_a[mae_best_pos], hist_u[mae_best_pos], hist_l[mae_best_pos], no_params[mae_best_pos]))
mape_best_pos = np.argmin(val_mape)
print("Best model based on MAPE is with %s architecture, %d units and %d layers (%d parameters)" 
       % (hist_a[mape_best_pos], hist_u[mape_best_pos], hist_l[mape_best_pos], no_params[mape_best_pos]))

d = {'Architecture': hist_a,
     'Layers': hist_l,
     'Units': hist_u,
     'Lambda': hist_lambda,
     'Validation MSE': val_mse,
     'Training MSE': mse}
df = pandas.DataFrame(data=d)
print(df)
