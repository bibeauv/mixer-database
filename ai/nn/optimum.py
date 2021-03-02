import MixerNN as MNN
import matplotlib.pyplot as plt
import numpy as np
import math
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

# =================================================================================
# Main program to verify the metrics of the optimum model

# Author: Valérie Bibeau, Polytechnique Montréal, 2020
# =================================================================================

# Read the data
data = MNN.read_mixerdata('mixer_database_0-9999.txt',19)

# Clean the data
data = MNN.clean_low_Re(data, 0.1, False)

# Set the features and the target values for the training and testing set
target_index = [0, 1, 2, 3, 4, 5, 6, 7]
X_train, X_test, y_train, y_test, scaler_X, scaler_y = MNN.initial_setup(data, 0.3, target_index, 8, 42)

# Compile and fit the optimum model
history, model, params = MNN.fit_model( X_train=X_train, y_train=y_train,
                                        no_features=len(target_index),
                                        learning_rate=0.1,
                                        l2=0.0,
                                        epochs=5000,
                                        val_frac=0.2,
                                        architecture='deep',
                                        units=18,
                                        layers=5,
                                        activation='tanh',
                                        verbose=0 )

# Save the model
model.save('optimum_mixer_model')

# Calculate the MAPE for the training set
train_predictions = model.predict(X_train)
mape = MNN.mean_absolute_percentage_error(y_true=scaler_y.inverse_transform(y_train),
                                          y_pred=scaler_y.inverse_transform(train_predictions))
# Calculate the metrics for the testing set
test_predictions = model.predict(X_test)
test_mse = mean_squared_error(y_true=y_test, y_pred=test_predictions)
test_mae = mean_absolute_error(y_true=y_test, y_pred=test_predictions)
test_mape = MNN.mean_absolute_percentage_error(y_true=scaler_y.inverse_transform(y_test),
                                               y_pred=scaler_y.inverse_transform(test_predictions))

print("Mean Squared Error:")
print("     Training set:   {:5.4e}".format(history.history['mse'][-1]))
print("     Validation set: {:5.4e}".format(history.history['val_mse'][-1]))
print("     Testing set:    {:5.4e}".format(test_mse))
print("Mean Absolute Error:")
print("     Training set:   {:5.6f}".format(history.history['mae'][-1]))
print("     Validation set: {:5.6f}".format(history.history['val_mae'][-1]))
print("     Testing set:    {:5.6f}".format(test_mae))
print("Mean Absolute Percentage Error:")
print("     Training set:   {:5.4f}".format(mape))
print("     Testing set:    {:5.4f}".format(test_mape))

# Make predictions
X_predict = np.array([[3, 1.4, 2.2, 3.5, 2.1,
                       0.1, math.pi/4,
                       2.6526]])
X_predict = scaler_X.transform(X_predict)
y_predict = model.predict(X_predict)
Np = scaler_y.inverse_transform(y_predict)
print("Predicted NP is: {:5.4f}".format(float(Np)))
print("True NP is: 21.729078")

X_predict = np.array([[2.5, 1.1, 4.3, 3.9, 3.1,
                       0.1, math.pi/4,
                       5.092958]])
X_predict = scaler_X.transform(X_predict)
y_predict = model.predict(X_predict)
Np = scaler_y.inverse_transform(y_predict)
print("Predicted NP is: {:5.4f}".format(float(Np)))
print("True NP is: 9.423747")

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Training', 'Validation'])
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.show()