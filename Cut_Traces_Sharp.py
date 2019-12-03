# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:23:56 2019

@author: Federica Lareno Faccini

This script is used to cut traces to the precise length of the recoridng.
It removes the extra random points added in the end of the recording.

"""

#from compute_timefreq import compute_timefreq
import numpy as np
import matplotlib.pyplot as plt

path = r'D:\F.LARENO.FACCINI\Preliminary Results\Ephy\Coordinate Hunting\852\RBF\Mock\P19\2019-10-03T18-28-36_mock_P19.rbf'
file = np.fromfile(path,dtype='float64').reshape(-1,16)


length = 9
sampling_rate = 20000
sigs = np.empty([(sampling_rate*length),16])
duration = 1/sampling_rate*len(sigs[:,0])
sig_times = np.arange(0,duration, 1/sampling_rate)

for i in range(len(file[0,:])):
    if len(file[:,i]) > (sampling_rate*length):
    
        sigs[:,i] = file[:,i][0:(sampling_rate*length)]
        print(len(sigs[:,i]))
        
    elif len(file[:,i]) == (sampling_rate*length):
        sigs[:,i] = file[:,i]
        
    else:
        print('Too few points in the channel {}, the recording may be corrupted'.format(i))
    
    
plt.plot(sig_times, sigs[:,0], linewidth=0.3, color='g')
plt.axvspan(6,7, color='skyblue')