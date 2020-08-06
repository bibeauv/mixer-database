import MixerNN as MNN
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

# Read the data
data = MNN.read_mixerdata('mixer_database_1-6250.txt')

# Clean the data
data = MNN.clean_low_Re(data, 0.1, True)

# Set the features and the target values for the training and testing set
X_train, X_test, y_train, y_test, scaler_X, scaler_y = MNN.initial_setup(data, 0.3)

# Try different model
num_params = []
mse = []
val_mse = []
test_mse = []
mae = []
val_mae = []
test_mae = []
for a in ['deep', 'cascade']:
    for l in [1, 2, 3, 4]:
        for u in [64, 128, 256, 512]:
            history, model, params = MNN.fit_model( X_train=X_train, y_train=y_train, 
                                                    learning_rate=0.1,
                                                    l2=0.0,
                                                    epochs=500,
                                                    val_frac=0.2,
                                                    architecture=a,
                                                    units=u,
                                                    layers=l )

            # Gather the number of parameters for each NN
            num_params.insert(len(num_params), params)

            # Gather the metrics for each NN
            mse.insert(len(mse), history.history['mse'][-1])
            val_mse.insert(len(val_mse), history.history['val_mse'][-1])
            test_mse.insert(len(test_mse), mean_squared_error(y_true=y_test, y_pred=model.predict(X_test)))
            mae.insert(len(mae), history.history['mae'][-1])
            val_mae.insert(len(val_mae), history.history['val_mae'][-1])
            test_mae.insert(len(test_mae), mean_absolute_error(y_true=y_test, y_pred=model.predict(X_test)))

print(mse)
print(val_mse)
print(test_mse)
print(mae)
print(val_mae)
print(test_mae)
print(num_params)