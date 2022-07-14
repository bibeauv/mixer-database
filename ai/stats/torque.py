import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

data1 = np.array([[0.03,		0.0016501928,	-0.0015031864,	-0.0004844229],			
[0.025,	    0.0016855793,	-0.0015340117,	-0.0004803311],	
[0.02,		0.0017268253,	-0.0015125890,	-0.0004787237],
[0.015,	    0.0017585343,	-0.0014556436,	-0.0004805770],
[0.01,		0.0017978850,	-0.0014414310,	-0.0004786837]])

data2 = np.array([[0.03,		0.0080101875,	-0.0083183166,	-0.0008427160],	
[0.025,	    0.0080963686,	-0.0082393840,	-0.0008408141],		
[0.02,		0.0082231465,	-0.0081686447,	-0.0008380965],
[0.015,	    0.0083212723,	-0.0080983573,	-0.0008368199],
[0.01,		0.0084506332,	-0.0080301660,	-0.0008353011]])

data3 = np.array([[0.03,		0.0002194192,	-0.0001447560,	-0.0000987476],
[0.025,	    0.0002241794,	-0.0001405604,	-0.0001060597],
[0.02, 		0.0002293931,	-0.0001386191,	-0.0001133080],
[0.015,	    0.0002344677,	-0.0001352490,	-0.0001189590],
[0.01,		0.0002394739,	-0.0001320885,	-0.0001224199]])

def plot_data(data,twin,ax,label):
    length = data[:,0]
    torque_int = data[:,1]
    
    # Richardson
    f1 = torque_int[np.where(length == 0.015)[0][0]]
    f2 = torque_int[np.where(length == 0.03)[0][0]]
    new_point_int = f1 + (f1 - f2) # si l'ordre du torque est de 1

    print((new_point_int-f2)/new_point_int*100)

    if not twin:
        fig,ax = plt.subplots()
        ax.plot(length,torque_int / np.min(torque_int),'-ob',label=label)
        #ax.plot(length,torque_ext,'-o',label='Walls')
        #ax.plot(np.append(length[-1],10**-10),np.append(torque_int[-1],new_point_int),'--k')
        ax.set_xscale('log')
        #ax.plot(np.append(length[-1],0),np.append(torque_ext[-1],new_point_ext),'--k')
        ax.grid(True,which='both')
        ax.set_ylabel(r'$\Gamma / \Gamma{min}$')
        ax.set_xlabel('Maximum characteristic length (m)')
        return ax
    elif twin:
        #ax2=ax.twinx()
        ax.plot(length,torque_int / np.min(torque_int),'-or',label=label)
        #ax2.plot(np.append(length[-1],10**-10),np.append(torque_int[-1],new_point_int),'--k')
        #ax2.set_xscale('log')
        #lines, labels = ax.get_legend_handles_labels()
        #lines2, labels2 = ax2.get_legend_handles_labels()
        #ax2.legend(lines + lines2, labels + labels2, loc=0)
        #ax2.grid(True,which='both')
        return ax
        
ax = plot_data(data2,False,None,'Average')
ax = plot_data(data3,True,ax,'Worse')
plt.legend()
plt.show()