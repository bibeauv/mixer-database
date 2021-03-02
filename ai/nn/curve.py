import MixerNN as MNN
import numpy as np
import math
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# =================================================================================
# Main program to verify a typical curve of Np vs Re

# Author: Valérie Bibeau, Polytechnique Montréal, 2020
# =================================================================================

# Load the model
model = keras.models.load_model('optimum_mixer_model')

# Set Reynolds
Reynolds = np.logspace(0,2,50)

# Get the data and clean it
data = MNN.read_mixerdata('mixer_database_0-9999.txt',19)
data = MNN.clean_low_Re(data, 0.1, False)

# Get the scaler
target_index = [0, 1, 2, 3, 4, 5, 6, 7]
X_train, X_test, y_train, y_test, scaler_X, scaler_y = MNN.initial_setup(data, 0.3, target_index, 8, 42)

# Predict Np with the model for different Re
Np_vec = []
for Re in Reynolds:
    # Fixed geometry with Reynolds
    geo = np.array([[3, 1, 4, 5, 5, 
                     0.1, 0, 
                     Re]])
    # Scale
    X_geo = scaler_X.transform(geo)
    # Predict
    Np = model.predict(X_geo)
    Np = scaler_y.inverse_transform(Np)
    Np_vec.insert(len(Np_vec), float(Np))

# Print the curve
Reynolds = Reynolds.tolist()

plt.scatter(Reynolds, Np_vec)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Re')
plt.ylabel('Np')
plt.show()