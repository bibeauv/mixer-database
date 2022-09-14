import MixerNN as MNN
import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras

# Read the data
data = MNN.read_mixerdata('mixer_database_0-99999.txt',19)

# Clean the data
data = MNN.clean_low_Re(data, 0.1, True)

# Set the features and the target values for the training and testing set
target_index = [0, 1, 2, 3, 5, 6, 7]
X_train, X_test, y_train, y_test, scaler_X, scaler_y = MNN.initial_setup(data, 0.01, target_index, 8, 42)

model = keras.models.load_model('optimum_mixer_model')

test_predictions = model.predict(X_test)

mape = MNN.mean_absolute_percentage_error(y_true=scaler_y.inverse_transform(y_test), 
                                          y_pred=scaler_y.inverse_transform(test_predictions))
print(mape)

a = plt.axes(aspect='equal')
plt.scatter(scaler_y.inverse_transform(y_test), scaler_y.inverse_transform(test_predictions),
            facecolors='none', edgecolors='b')
lims = [0,60]
plt.plot(lims,lims,'-k')
plt.xlabel('True Values [Np]')
plt.ylabel('Predictions [Np]')
plt.show()

error = scaler_y.inverse_transform(test_predictions) - scaler_y.inverse_transform(y_test)
plt.hist(error, bins=25)
plt.xlabel('Prediction Error [Np]')
plt.ylabel('Count')
plt.show()