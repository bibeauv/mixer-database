import MixerNN as MNN
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# =================================================================================
# Main program to verify a typical curve of Np vs Re

# Author: Valérie Bibeau, Polytechnique Montréal, 2020
# =================================================================================
# ---------- Index ----------
# 0: T/D    1: H/T      2: T/C      3: D/W      4: D/W_hub
# 5: E      6: theta    7: omega    8: Re       9: Np

# Load the model
model = keras.models.load_model('optimum_mixer_model')

# Set Reynolds
Reynolds = np.logspace(0,2,100)

# Get the data and clean it
data = MNN.read_mixerdata('mixer_database_1-6250.txt')
data = MNN.clean_low_Re(data, 0.1, True)

# Get the scaler
target_index = [0, 1, 2, 3, 4, 8]
X_train, X_test, y_train, y_test, scaler_X, scaler_y = MNN.initial_setup(data, 0.3, target_index, 42)

# Predict Np with the model for different Re
Np_vec = []
for Re in Reynolds:
    # Fixed geometry with Reynolds
    geo = np.array([[3, 1, 2, 4, 4, Re]])
    # Scale
    X_geo = scaler_X.transform(geo)
    # Predict
    Np = model.predict(X_geo)
    Np = scaler_y.inverse_transform(Np)
    Np_vec.insert(len(Np_vec), float(Np))

print(Np_vec)

# Print the curve
Reynolds = Reynolds.tolist()

plt.scatter(Reynolds, Np_vec)
plt.xlabel('Re')
plt.ylabel('Np')
plt.show()