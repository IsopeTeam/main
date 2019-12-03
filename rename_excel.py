# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 21:49:17 2019

@author: F.LARENO-FACCINI
"""
import glob
import os
#import pandas as pd

#Import all the files, by creating a list of them
files = glob.glob('D:/F.LARENO.FACCINI/Preliminary Results/Ephy/5101 (Atlas - Male)/Power Values/Light Stim/*.xlsx')
names = [os.path.basename(x) for x in files]

path = (r'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/5101 (Atlas - Male)/Power Values/Light Stim/')
mouse = 5101

for f in range(len(names)):
    
    old_file = os.path.join(path, names[f])
    new_file = os.path.join(path, '{}_{}'.format(mouse,names[f]))
    os.rename(old_file, new_file)