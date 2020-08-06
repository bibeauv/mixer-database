# ============================================================================
# Neural Network functions using TensorFlow
# Goal : Predict the number of power of the impeller of a mixer.
# Author : Valérie Bibeau, Polytechnique Montréal, 2020
# ============================================================================

# ----------------------------------------------------------------------------
# Arrays for data
import numpy as np
# To normalize data
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
# NN
import numpy as np
np.random.seed(1)               # for reproducibility
import tensorflow
tensorflow.random.set_seed(2)   # for reproducibility
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout

# ----------------------------------------------------------------------------
def read_mixerdata(file_name):
    """Read the data of the mixers

    Args:
        file_name (string): Name of the file that contains the data

    Returns:
        data (array): Mixers' dataset
    """
    dataset = open(file_name,'r')
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
    return data

def clean_low_Re(data, treshold, enable):
    """Clean the data to remove the outliers (low Reynolds)

    Args:
        data (array): The dataset that need to be cleaned
        treshold (float): Treshold of the lower Reynolds accepted
        enable (bool): If true, the cleaning will occur

    Returns:
        data (array): Mixers' dataset cleaned
    """
    if enable == True:
        data_list = data.tolist()
        m = 0
        while m < len(data_list):
            if data_list[m][8] < treshold:
                data_list.pop(m)
            else:
                m = m + 1
        data = np.array(data_list)
    return data

def initial_setup(data, test_size):
    """Set up the training and testing set

    Args:
        data (array): Mixers' dataset
        test_size (float): Fraction of the training set that will be tested

    Returns:
        X and y: Features and target values of the training and testing set
    """
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
    X_train, X_test, y_train, y_test = train_test_split(Xscale, yscale, 
                                                        test_size=test_size,
                                                        random_state=42)
    return X_train, X_test, y_train, y_test, scaler_X, scaler_y

def fit_model(X_train, y_train, learning_rate, l2, epochs, val_frac, architecture, units, layers):
    """Neural Network architecture/model to train the mixers

    Args:
        X_train and y_train: Features and target values of the training set
        learning_rate (float): Learning rate of the gradient descent
        l2 (float): Regularization constant
        epochs (int): Number of iterations
        val_frac (float): Fraction of the training that will serve the validation of the model
        architecture (string): Type of the architecture
        units (int): Number of units of the first hidden layer
        layers (int): Number of layers in the NN

    Returns:
        history: History of the algorithme
    """
    # Optimizer
    opt = keras.optimizers.Adagrad(learning_rate=learning_rate)
    # Initializer
    ini = keras.initializers.GlorotUniform()
    # Regularizer
    reg = keras.regularizers.l2(l2)
    # Architecture of the Neural Network
    if architecture == 'deep':
        model = Sequential()
        model.add(Dense(units, input_dim=8, kernel_initializer=ini, activation='relu'))
        l = 1
        while l <= layers:
            model.add(Dense(units, kernel_initializer=ini, activation='relu'))
            l = l + 1
        model.add(Dense(1,     kernel_initializer=ini, activation='linear'))
    elif architecture == 'cascade':
        model = Sequential()
        model.add(Dense(units, input_dim=8, kernel_initializer=ini, activation='relu'))
        l = 1
        while l <= layers and units >= 2:
            units = units/2
            model.add(Dense(units, kernel_initializer=ini, activation='relu'))
            l = l + 1
        model.add(Dense(1,     kernel_initializer=ini, activation='linear'))        
    # Compile and Fit
    model.compile(loss='mse', optimizer=opt, metrics=['mse','mae','mape'])
    model.summary()
    history = model.fit(X_train, y_train, epochs=epochs, validation_split=val_frac, verbose=0)
    return history, model, model.count_params()

def mean_absolute_percentage_error(y_true, y_pred):
    """Mean Absolute Percentage Error

    Args:
        y_true (array): True values
        y_pred (array): Predicted values

    Returns:
        mape
    """
    diff = np.abs((y_true - y_pred) / y_true)
    mape = np.mean(diff) * 100
    return mape