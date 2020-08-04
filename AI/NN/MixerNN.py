# ============================================================================
# Neural Network, TensorFlow
# Predict the number of power of the impeller of a mixer.
# Author : Valérie Bibeau, Polytechnique Montréal, 2020
# ============================================================================

# ----------------------------------------------------------------------------
# Arrays for data
import numpy as np
# To normalize data
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
# NN
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
# Visualization
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Read the data
dataset = open('mixer_database_1-6250.txt','r')

mixer = dataset.readlines()

for m in np.arange(0, len(mixer)-1, dtype=int):
    x = np.array([])
    features = mixer[m].split('\t')
    for f in np.arange(2,21,2):
        x = np.insert(x, len(x), float(features[f]))
    if m == 0:
        data = x
    else:
        data = np.vstack((data, x))

# Clean the data by removing the outliers (low Reynolds)
data_list = data.tolist()
m = 0
while m < len(data_list):
    if data_list[m][8] < 0.1:
        data_list.pop(m)
    else:
        m = m + 1
data = np.array(data_list)

# Separate features from target values (omega is skipped)
X = data[:,[0, 1, 2, 3, 4, 5, 6, 8]]
y = data[:,9]
y = np.reshape(y, (-1, 1))

# Normalizing features
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
scaler_X.fit(X)
scaler_y.fit(y)
Xscale = scaler_X.transform(X)
yscale = scaler_y.transform(y)

# Split the data into training and testing
X_train, X_test, y_train, y_test = train_test_split(Xscale, yscale, test_size=0.25)

# ----------------------------------------------------------------------------
# Keras Model Configuration
# Optimizer
opt = keras.optimizers.Adagrad(learning_rate=0.1)

# Initializer
ini = keras.initializers.GlorotUniform()

# Architecture of the Neural Network
model = Sequential()
model.add(Dense(128, input_dim=8, kernel_initializer=ini ,activation='relu'))
model.add(Dense(64, kernel_initializer=ini, activation='relu'))
model.add(Dense(32, kernel_initializer=ini, activation='relu'))
model.add(Dense(1,  kernel_initializer=ini, activation='linear'))

# Compile and Fit
model.compile(loss='mse', optimizer=opt, metrics=['mse','mae'])

model.summary()

history = model.fit(X_train, y_train, epochs=1500)

# Loss over iterations
plt.plot(history.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.show()

# ----------------------------------------------------------------------------
# Verify the model with the testing data
test_predictions = model.predict(X_test).flatten()
a = plt.axes(aspect='equal')
plt.scatter(y_test, test_predictions)
plt.xlabel('True values')
plt.ylabel('Predictions')
plt.show()

# Make predictions
Xnew = np.array([[3, 1.4, 2.2, 3.5, 2.1, 0.1, 0.785398, 2.6526]])
Xnew = scaler_X.transform(Xnew)
ynew = model.predict(Xnew)
ynew = scaler_y.inverse_transform(ynew)
print(ynew)
print(21.729078)

Xnew = np.array([[2.5, 1.1, 4.3, 3.9, 3.1, 0.1, 0.785398, 5.092958]])
Xnew = scaler_X.transform(Xnew)
ynew = model.predict(Xnew)
ynew = scaler_y.inverse_transform(ynew)
print(ynew)
print(9.423747)