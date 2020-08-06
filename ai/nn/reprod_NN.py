import MixerNN as MNN
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

# =================================================================================
# Main program to verify the reproductibility of the optimum
# with different training and testing set

# Author: Valérie Bibeau, Polytechnique Montréal, 2020
# =================================================================================
# ---------- Index ----------
# 0: T/D    1: H/T      2: T/C      3: D/W      4: D/W_hub
# 5: E      6: theta    7: omega    8: Re       9: Np

# Read the data
data = MNN.read_mixerdata('mixer_database_1-6250.txt')

# Clean the data
data = MNN.clean_low_Re(data, 0.1, True)

# Try different model
no_params = []
mse = []
val_mse = []
test_mse = []
mae = []
val_mae = []
test_mae = []
mape = []
val_mape = []
test_mape = []
for rep in np.arange(0,20):
    # Set the features and the target values for the training and testing set
    target_index = [0, 1, 2, 3, 4, 5, 6, 8]
    X_train, X_test, y_train, y_test, scaler_X, scaler_y = MNN.initial_setup(data, 0.3, target_index, rep)
    
    # Fit the model
    history, model, params = MNN.fit_model( X_train=X_train, y_train=y_train,
                                            no_features=len(target_index),
                                            learning_rate=0.1,
                                            l2=0.0,
                                            epochs=2000,
                                            val_frac=0.2,
                                            architecture='cascade',
                                            units=512,
                                            layers=4,
                                            verbose=0 )
    # Gather the number of parameters
    no_params.insert(len(no_params), params)

    # Gather the metrics for each NN
    mse.insert(len(mse), history.history['mse'][-1])
    val_mse.insert(len(val_mse), history.history['val_mse'][-1])
    test_mse.insert(len(test_mse), mean_squared_error(y_true=y_test, y_pred=model.predict(X_test)))
    mae.insert(len(mae), history.history['mae'][-1])
    val_mae.insert(len(val_mae), history.history['val_mae'][-1])
    test_mae.insert(len(test_mae), mean_absolute_error(y_true=y_test, y_pred=model.predict(X_test)))
    mape.insert(len(mape), history.history['mape'][-1])
    val_mape.insert(len(val_mape), history.history['val_mape'][-1])
    y_pred = model.predict(X_test)
    y_pred = scaler_y.inverse_transform(y_pred)
    test_mape.insert(len(test_mape), MNN.mean_absolute_percentage_error(y_true=scaler_y.inverse_transform(y_test),
                                                                        y_pred=y_pred))

plt.figure(1)
plt.scatter(np.arange(0,20), mse)
plt.scatter(np.arange(0,20), val_mse)
plt.scatter(np.arange(0,20), test_mse)
plt.legend(['Training set','Validation set','Testing set'])
plt.title('MSE')

plt.figure(2)
plt.scatter(np.arange(0,20), mae)
plt.scatter(np.arange(0,20), val_mae)
plt.scatter(np.arange(0,20), test_mae)
plt.legend(['Training set','Validation set','Testing set'])
plt.title('MAE')

plt.figure(3)
plt.scatter(np.arange(0,20), mape)
plt.scatter(np.arange(0,20), val_mape)
plt.scatter(np.arange(0,20), test_mape)
plt.legend(['Training set','Validation set','Testing set'])
plt.title('MAPE')

plt.show()