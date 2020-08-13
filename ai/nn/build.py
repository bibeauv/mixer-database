import MixerNN as MNN
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

# =================================================================================
# Main program to find and build the model that has a better performance

# Author: Valérie Bibeau, Polytechnique Montréal, 2020
# =================================================================================
# ---------- Index ----------
# 0: T/D    1: H/T      2: T/C      3: D/W      4: D/W_hub
# 5: E      6: theta    7: omega    8: Re       9: Np

# Read the data
data = MNN.read_mixerdata('mixer_database_1-6250.txt')

# Clean the data
data = MNN.clean_low_Re(data, 0.1, True)

# Set the features and the target values for the training and testing set
target_index = [0, 1, 2, 3, 4, 5, 6, 8]
X_train, X_test, y_train, y_test, scaler_X, scaler_y = MNN.initial_setup(data, 0.3, target_index, 42)

# Try different model
no_params = []
val_mse = []
val_mae = []
val_mape = []
hist_a = []
hist_l = []
hist_u = []
for a in ['deep', 'cascade']:
    for l in [1, 2, 3, 4]:
        for u in [64, 128, 256, 512]:
            history, model, params = MNN.fit_model( X_train=X_train, y_train=y_train,
                                                    no_features=len(target_index),
                                                    learning_rate=0.1,
                                                    l2=0.0,
                                                    epochs=500,
                                                    val_frac=0.2,
                                                    architecture=a,
                                                    units=u,
                                                    layers=l,
                                                    verbose=0 )
            # Trace the history
            hist_a.insert(len(hist_a), a)
            hist_l.insert(len(hist_l), l)
            hist_u.insert(len(hist_u), u)

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