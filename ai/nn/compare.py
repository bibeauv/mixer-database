import math
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

# Load the model
model = keras.models.load_model('optimum_mixer_model')

# Predict testing set
y_pred = model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred)

fic = open('corr_sim_nn.txt','w')
fic.write('Corr\tSim\tNN\n')
mixers = np.arange(0, len(y_pred))
for m in mixers:
    # NN
    NP_nn = y_pred[m][0]

    mixer = scaler_X.inverse_transform(X_test)
    # Correlation
    d = mixer[m][0]**-1
    H = mixer[m][1]**1
    b = d/(mixer[m][3])
    Red = mixer[m][-1]
    NP_corr = correlation(b, d, H, Red)

    # Simulation
    NP_sim = scaler_y.inverse_transform([y_test[m]])

    # Write
    fic.write('%.2f\t%.2f\t%.2f\n' % (NP_corr, NP_sim, NP_nn))
fic.close()