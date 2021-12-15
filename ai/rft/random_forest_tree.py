import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold

# ---------- Read the data without the ratio ----------
with open('mixer_database_0-9999.txt', 'r') as f:
    lines = f.readlines()

X = []
y = []
T = 1
for line in lines:
    features = line.split('\t')
    if features[-1] != '!SIMULATION FAILED!\n':
        D = T / float(features[2])
        H = float(features[4]) * T
        C = T / float(features[6])
        W = D / float(features[8])
        W_hub = D / float(features[10])
        E = float(features[12]) * W
        theta = float(features[14])
        Re = float(features[16])
        X.append([D, H, C, W, W_hub, E, theta, Re])
        Np = float(features[18].split('\n')[0])
        y.append([Np])

# ---------- Normalization ----------
X = np.array(X)
X_norm = deepcopy(np.transpose(X))
y = np.array(y)
list_scaler = []
for f in range(len(X_norm)):
    scaler = MinMaxScaler()
    scaler.fit(X_norm[f].reshape(-1,1))
    new_X = scaler.transform(X_norm[f].reshape(-1,1))
    X_norm[f] = new_X.reshape(1, len(X))
    list_scaler.append(scaler)
    del scaler

X_norm = np.transpose(X_norm)
y_norm = y.reshape(1, len(y))[0]

# ---------- Random forest regressor ----------
regr = RandomForestRegressor(n_estimators=100, random_state=0)
regr.fit(X_norm, y_norm)
print('Score on training set:')
print(regr.score(X_norm, y_norm))

# ---------- Predictions for one geometry ----------
sorted_X = X[np.argsort(X[:,-1])]
X_to_predict = X_norm[np.argsort(X[:,-1])]
random_geo = np.random.choice(range(len(X)))
for i in range(len(X_to_predict)):
    X_to_predict[i] = np.concatenate((X_to_predict[random_geo][0:-1], np.array([X_to_predict[i][-1]])), axis=None)
pred_Np = regr.predict(X_to_predict)
plt.plot(sorted_X[:,-1], pred_Np)
plt.yscale("log")
plt.xscale("log")
plt.legend(['Training', 'Predictions'])
plt.xlabel('Reynolds')
plt.ylabel('Number of power')
plt.show()

# ---------- Cross validation ----------
kf = KFold(n_splits=5)
i = 1
for train, test in kf.split(X_norm):
    regr.fit(X_norm[train], y_norm[train])
    print('Score on ' + str(i) + ' fold: ' + str(regr.score(X_norm[test], y_norm[test])))
    i += 1
