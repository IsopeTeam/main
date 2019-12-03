# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 17:04:02 2019
Concatenates separated files (raw binary) in one single file
@author: lspaeth
"""

import os 
import numpy as np 
from matplotlib import pyplot as plt

#--------------------FILL THIS INFO BEFORE RUNNING----------------------------
nb_channel = 16
sample_rate = 20000
t_start=0

#The folder to pick up the data
folder = 'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Coordinate Hunting/855/RBF/VII/P19/'

file_save = folder + 'concatenate.rbf'

#-----------------------------------------------------------------------------

#Lists all files in folder 
list_dir = os.listdir(folder)

for file, idx in zip(list_dir, range(len(list_dir))):
    
    if file.endswith('.rbf'):
   
        new_path = folder+file
        
        sigs = np.fromfile(new_path,dtype='float64').reshape(nb_channel,-1)
        
        print([idx])
        
        if idx == 0:
           
            _all = sigs
        
        else:
            _all = np.concatenate((_all,sigs), axis=1)
            
    else :
        continue

#Save the file 

with open(file_save, mode='wb') as file : 
    _all.tofile(file_save,sep='')