# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 18:02:00 2019

@author: F.LARENO-FACCINI
"""

import pandas as pd
import glob
import os
import openpyxl



protocol = 'P13'
condition = 'No stim'
power = 'High'


#Import all the files, by creating a list of them
files = glob.glob('D:/F.LARENO.FACCINI/Preliminary Results/Ephy/6336 (Atlas - Male)/Power Values/Valve/20 mW/{}/{}/{}/*.xlsx'.format(protocol,power,condition))
names = [os.path.basename(x) for x in files]

#Remove the extension from the name in the list
for x in range(len(names)):
    names[x] = names[x].replace(".xlsx","")


for f in range(len(names)):
    
    file_path = 'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/6336 (Atlas - Male)/Power Values/Valve/20 mW/{}/{}/{}/{}.xlsx'.format(protocol,power,condition,names[f])    

    try:   
        ss = openpyxl.load_workbook(file_path) 
        sb_sheet = ss.get_sheet_by_name('Before (500ms)')
        sb_sheet.title = 'Before (500 ms)'
        ss.save(file_path)
#        sd_sheet = ss.get_sheet_by_name('During (500ms)')
#        sd_sheet.title = 'During (500 ms)'
#        ss.save(file_path)
        sa_sheet = ss.get_sheet_by_name('After (500ms)')
        sa_sheet.title = 'After (500 ms)'
        ss.save(file_path)
    except:
        continue

for f in range(len(names)):
    
    file_path = 'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/6336 (Atlas - Male)/Power Values/Valve/20 mW/{}/{}/{}/{}.xlsx'.format(protocol,power,condition,names[f])    
   
    before = pd.read_excel(file_path, sheet_name='Before (500 ms)', ).drop(['Unnamed: 0'],axis=1)
#    during = pd.read_excel(file_path, sheet_name='During (500 ms)').drop(['Unnamed: 0'],axis=1)
    after = pd.read_excel(file_path, sheet_name='After (500 ms)').drop(['Unnamed: 0'],axis=1)
    
    if f==0:
        df1 = before
#        df2 = during
        df3 = after
    else:
        df1 = pd.concat([df1,before], axis=1)
#        df2 = pd.concat([df2,during], axis=1)
        df3 = pd.concat([df3,after], axis=1)


powerdir = (r'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/6336 (Atlas - Male)/Power Values/Valve/')
  
with pd.ExcelWriter('{}/20mW_{}_{}_{}_tot.xlsx'.format(powerdir,protocol,condition,power), engine='openpyxl') as writer:
                       
    df1.to_excel(writer, sheet_name='Before (500 ms)', index=False)
#    df2.to_excel(writer, sheet_name='During (500 ms)', index=False)
    df3.to_excel(writer, sheet_name='After (500 ms)', index=False)
