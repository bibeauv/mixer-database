import math
import matplotlib.pyplot as plt
import numpy as np
import MixerNN as MNN
from tensorflow import keras

# ------------------------------------------------------------------------------------------
# http://downloads.hindawi.com/journals/ijce/2012/106496.pdf

# b: Height of impeller blade
# C: Clearance between bottom and impeller
# D: Vessel diameter
# d: Impeller diameter
# f: Friction factor
# H: Liquid depth
# hb: Baffle lenght
# NP: Power number
# NP0: Power number in unbaffled condition
# NPMax: Power number in fully baffed condition
# n: Impeller rotational speed
# nb: Number of baffle plates
# np: Number of blades
# Red: Reynolds number
# ReG: Modifed Reynolds number
# T: Shaft torque
# theta: Angle of impeller blade
# mu: Viscosity
# rho: Density

def correlation(b, d, H, Red):
    # Constants
    D = 1
    np = 4
    theta = math.pi/4

    # Variables
    eta = 0.711*(0.157 + (np*math.log(D/d))**0.611)/(np**0.52*(1 - (d/D)**2))
    beta = 2*math.log(D/d)/((D/d) - (d/D))
    gamma = (eta*math.log(D/d)/((beta*D/d)**5))**(1/3)
    X = gamma*np**0.7*b*(math.sin(theta/H))**1.6

    Ct = ((1.96*X**1.19)**-7.8 + (0.25)**-7.8)**(-1/7.8)
    Ctr = 23.8*(d/D)**-3.24*(b*math.sin(theta/D))**-1.18*X**-0.74
    Cl = 0.215*eta*np*(d/H)*(1 - (d/D)**2) + 1.83*(b*math.sin(theta/H))*(np/(2*math.sin(theta)))**(1/3)
    m = ((0.71*X**0.373)**-7.8 + (0.333)**-7.8)**(-1/7.8)

    ff = 0.0151*(d/D)*Ct**0.308
    ReG = (math.pi*eta*math.log(D/d)/(4*d/beta/D))*Red

    f = Cl/ReG + Ct*(((Ctr/ReG) + ReG)**-1 + (ff/Ct)**(1/m))**m

    NP0 = ((1.2*math.pi**4*beta**2)/(8*d**3/(D**2*H)))*f

    return NP0
# ------------------------------------------------------------------------------------------

# Read the data
data = MNN.read_mixerdata('mixer_database_1-1024.txt',19)

# Clean the data
data = MNN.clean_low_Re(data, 0.1, False)

# Set the features and the target values for the training and testing set
target_index = [0, 1, 2, 3, 4, 5, 6, 7]
X_train, X_test, y_train, y_test, scaler_X, scaler_y = MNN.initial_setup(data, 0.3, target_index, 8, 42)

# Load the model
model = keras.models.load_model('optimum_mixer_model')

# Predict testing set
y_pred = model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred)

# Set Reynolds
Reynolds = np.logspace(0,2,50)*2

# Predict Np with the model for different Re
Np_vec = []
Np0_vec = []
for Re in Reynolds:
    # Fixed geometry with Reynolds
    geo = np.array([[3, 1, 3, 4, 4, 
                     0.1, math.pi/4, 
                     Re]])
    # Scale
    X_geo = scaler_X.transform(geo)
    # Predict
    Np = model.predict(X_geo)
    Np = scaler_y.inverse_transform(Np)
    Np_vec.insert(len(Np_vec), float(Np))
    # Correlation
    d = geo[0][0]**-1
    H = geo[0][1]**1
    b = d/geo[0][3]
    Red = Re
    Np_corr = correlation(b, d, H, Red)
    Np0_vec.insert(len(Np0_vec), Np_corr)

# Print the curve
Reynolds = Reynolds.tolist()

plt.scatter(Reynolds, Np_vec)
plt.scatter(Reynolds, Np0_vec)
plt.legend(['Predictions', 'Correlation'])
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Re')
plt.ylabel('Np')
plt.show()