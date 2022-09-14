from re import L
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

epochs = [1000]
layers = [2,3,4,5]
neurons = [50,60,70,80,90,100]
batch_size = [100, 500, 1000]

df = pd.read_excel('grid_search2.xlsx')

#%% Pour une architecture donnée, MSE/batch size pour différents epochs

df1 = df[(df['neurons'] == 50) & (df['layers'] == 3)]

for epoch in epochs:
    dff = df1[(df1['epochs'] == epoch)]
    bs = dff['batch_size'].to_numpy()
    mse = dff['mean'].to_numpy()
    mse = np.abs(mse)
    plt.plot(bs, mse, '-o', label=f'{epoch} epochs')
    
plt.legend()
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Batch size')
plt.ylabel('MSE')
plt.show()

#%% Pour un batch size donné et un nombre d'epochs donné, MSE/batch size pour différents nombres de neurones

df2 = df

params = df2['neurons']*7 + (df2['layers']-1)*df2['neurons']**2 + df2['neurons']*1
df2['params'] = params

for epoch in epochs:
    for bs in batch_size:
        dff = df2[(df2['epochs'] == epoch) & (df2['batch_size'] == bs)]
        dff = dff.sort_values('mean')
        min_mse_param = dff.iloc[-1]['params']
        print(f'with {epoch} epochs and {bs} batch size, min MSE is with {min_mse_param} parameters')

ax = plt.subplot()

plot_hist = {'1000-2000':[],
             '2000-5000':[],
             '5000-10000':[],
             '10000-20000':[],
             '20000-50000':[]}
labels=[]
for epoch in epochs:
    for bs in batch_size:
        labels.append(f'epochs={epoch},batch_size={bs}')
        dff = df2[(df2['epochs'] == epoch) & (df2['batch_size'] == bs)]
        hist = {'1000-2000':[],
                '2000-5000':[],
                '5000-10000':[],
                '10000-20000':[],
                '20000-50000':[]}
        for i in range(len(dff)):
            for j in range(len(hist)):
                k = list(hist.keys())[j]
                min_param = float(k.split('-')[0])
                max_param = float(k.split('-')[1])
                if dff.iloc[i]['params'] >= min_param and dff.iloc[i]['params'] <= max_param:
                    hist[k].append(np.abs(dff.iloc[i]['mean']))        
        for j in range(len(plot_hist)):
            k = list(plot_hist.keys())[j]
            plot_hist[k].append(np.mean(np.array(hist[k])))

ind = np.arange(len(plot_hist))
w = 0.1
for j in range(len(epochs)*len(batch_size)):
    ax.bar(ind+w*j,np.array(list(plot_hist.values()))[:,j],width=0.1,align='center',label=labels[j])
ax.set_xticks(ind+w*len(epochs)*len(batch_size)/2)
ax.set_xticklabels(plot_hist.keys())
ax.set_yscale('log')
ax.legend()
plt.show()
