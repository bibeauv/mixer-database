import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler


def read_mixerdata(file_name, col):
    """Read the data of the mixers

    Args:
        file_name (string): Name of the file that contains the data

    Returns:
        data (array): Mixers' dataset
    """
    dataset = open(file_name,'r')
    mixer = dataset.readlines()
    for m in np.arange(0, len(mixer), dtype=int):
        x = np.array([])
        features = mixer[m].split('\t')
        if features[-1] != '!SIMULATION FAILED!\n':
            for f in np.arange(2,col,2):
                x = np.insert(x, len(x), float(features[f]))
            if m == 0:
                data = x
            else:
                data = np.vstack((data, x))
    return data

# Read data
data = read_mixerdata('mixer_database_0-19999.txt', 19)
data_dict = {'TD':data[:,0],
             'HT':data[:,1],
             'TC':data[:,2],
             'DW':data[:,3],
             'EW':data[:,5],
             'theta':data[:,6],
             'Re':data[:,7],
             'Np':data[:,8]}
data_df = pd.DataFrame(data_dict)

# Correlation
# correlation = data_df.corr()
# print(correlation)
# plt.matshow(correlation)
# plt.colorbar()
# plt.show()

# PCA
# pca = PCA(n_components=3)
# X = data[:,0:-1]
# y = np.array(data[:,-1]).reshape(-1,1)
# pca.fit(X)
# new_features = pca.fit_transform(X)
# print(new_features)

# Covariance
new_data = np.delete(data,4,axis=1)
scaler = MinMaxScaler()
scaler.fit(new_data)
scaled_data = scaler.transform(new_data)
cov_matrix = np.cov(np.transpose(scaled_data))
# u, s, vh = np.linalg.svd(cov_matrix)
eigen_values, eigen_vectors = np.linalg.eig(cov_matrix)
index = {0:'TD',
         1:'HT',
         2:'TC',
         3:'DW',
         4:'EW',
         5:'theta',
         6:'Re',
         7:'Np'}
for i in range(8):
    print(f"{i}e valeur propre = ", eigen_values[i])
    print(f"{i}e vecteur propre = ", eigen_vectors[i])