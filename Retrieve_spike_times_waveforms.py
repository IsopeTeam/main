# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 18:11:04 2019

@author: Sam Garcia
"""
from matplotlib import pyplot as plt 
import tridesclous as tdc 
import numpy as np

dataio = tdc.DataIO('D:/F.LARENO.FACCINI/Preliminary Results/Ephy/2535 (Baseline of 3s - Atlas)/HDF5/1300/P2/rbf/Concatenate/conc/tdc_2019-03-06T17-54-30Concatenate_1300um_P2/')

cc = tdc.CatalogueConstructor(dataio, chan_grp=0) 
print (cc.all_peaks['cluster_label']) # contient le clucter 
print(cc.all_peaks['index']) # contient la position cc.all_peaks['segment'] # 

sampling_period = 1.0/20000

clust_id = cc.all_peaks['cluster_label']

spike_times = cc.all_peaks['index']*sampling_period



plt.figure()
#colors = ['b','r','orange','green','blue']

for i in range(len(spike_times)):    
    plt.scatter(spike_times[i],1, #color=colors[clust_id[i]])
    
    
waveforms_label = cc.clusters['cluster_label']

waveforms = cc.centroids_median

print (waveforms)

plt.figure()
plt.plot(waveforms[0])

single_wf = waveforms[0].reshape(-1,4)
plt.figure()
plt.plot(single_wf[:,0])
