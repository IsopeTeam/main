# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 14:41:30 2019

@author: F.LARENO-FACCINI
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

############################################################################### 
##------------------------------ Before vs. After ---------------------------##
###############################################################################

 
files = glob.glob('D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Power values/Second Cue/*.xlsx')
name = [os.path.basename(x)  for x in files]

names = []

#Remove the extension from the name in the list
for x in range(len(name)):
    name[x] = name[x].replace(".xlsx","")
    if 'No stim_Low' in name[x]:
        names.append(name[x])
    else:
        continue


for file in range(len(names)):

    file_path = 'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Power values/Second Cue/{}.xlsx'.format(names[file])
    
    before = pd.read_excel(file_path, sheet_name='Before (500 ms)')
    before = before.transpose()
    before = before.values
          
    during = pd.read_excel(file_path, sheet_name='During (500 ms)')
    during = during.transpose()
    during = during.values
    
    after = pd.read_excel(file_path, sheet_name='After (500 ms)')
    after = after.transpose()
    after = after.values
    
    
    fig,ax = plt.subplots(1,1, figsize=(15,10))
    
    
    bp = ax.boxplot(before,patch_artist=True, showfliers=False, positions=np.arange(before.shape[1])-.2, widths=0.4)  
    dp = ax.boxplot(during,patch_artist=True, showfliers=False, positions=np.arange(before.shape[1]), widths=0.2)    
    ap = ax.boxplot(after, patch_artist=True, showfliers=False, positions=np.arange(before.shape[1])+.2, widths=0.4)


    ax.set_xticks(np.arange(len(before[0])))
    if len(before[1]) > 30:
        ax.set_xticklabels(np.arange(32,81,1))
    else:
        ax.set_xticklabels(np.arange(1,21,1))
        
    ax.set_xlim(-0.5,len(before[0])-.5)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power (V/Hz)')
    ax.set_title(names[file])

#    plt.savefig('D:\F.LARENO.FACCINI\Preliminary Results\Ephy\Power values\Figures\Before vs After\Light Stim\{}.pdf'.format(names[file]))
#    plt.close()  
    

#-------------------------- Extracting the MEDIAN ----------------------------


    bp_med, dp_med, ap_med = [], [], []

    for medline in bp['medians']:
        linedata = medline.get_ydata()
        median = linedata[0]
        bp_med.append(median)
    for medline in dp['medians']:
        linedata = medline.get_ydata()
        median = linedata[0]
        dp_med.append(median)
    for medline in ap['medians']:
        linedata = medline.get_ydata()
        median = linedata[0]
        ap_med.append(median)

        
    if file == 0:
        bpf = pd.DataFrame(bp_med, index=None, columns=[names[file]])
        dpf = pd.DataFrame(dp_med, index=None, columns=[names[file]])
        apf = pd.DataFrame(ap_med, index=None, columns=[names[file]])

    else:
        bpf[names[file]] = pd.DataFrame(bp_med, index=None)
        dpf[names[file]] = pd.DataFrame(dp_med, index=None)
        apf[names[file]] = pd.DataFrame(ap_med, index=None)

#    save_dir = 'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Power values/rbf with different time windows for control/Fake_P15_Low'
#
#    with pd.ExcelWriter('{}/Median_LightStim_fakeP15_Low_BvsA.xlsx'.format(save_dir), engine='openpyxl') as writer:
#                           
#        bpf.to_excel(writer, sheet_name='Before', index=False, header=True)
#        dpf.to_excel(writer, sheet_name='During', index=False, header=True)
#        apf.to_excel(writer, sheet_name='After', index=False, header=True)



###############################################################################
##---------------------------- Stim vs. No Stim (2 sheets) ------------------##
###############################################################################


#files = glob.glob('D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Power values - Copy/Valve/*.xlsx')
#names = [os.path.basename(x)  for x in files]
#
#nostim = []
#stim = []
#
##Remove the extension from the name in the list
#
#for x in range(len(names)):
#    names[x] = names[x].replace(".xlsx","")
#    if 'No' in names[x]:
#        nostim.append(names[x])
#    else:
#        stim.append(names[x])
#
#
#for file in range(len(stim)):
#    
#    fig, ax = plt.subplots(2,1, figsize=(15,10), sharey=True)
#   
#    stim_path = 'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Power values - Copy/Valve/{}.xlsx'.format(stim[file])
#    nostim_path = 'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Power values - Copy/Valve/{}.xlsx'.format(nostim[file])
#    
#    print(stim_path)
#    print(nostim_path)
#    print('--------------------------------------------------')
#    
#    stim_before = pd.read_excel(stim_path, sheet_name='Before (500 ms)')
#    stim_before = stim_before.transpose()
#    stim_before = stim_before.values
#
#    nostim_before = pd.read_excel(nostim_path, sheet_name='Before (500 ms)')
#    nostim_before = nostim_before.transpose()
#    nostim_before = nostim_before.values
#    
#    stim_after = pd.read_excel(stim_path, sheet_name='After (500 ms)')
#    stim_after = stim_after.transpose()
#    stim_after = stim_after.values
#    
#    nostim_after = pd.read_excel(nostim_path, sheet_name='After (500 ms)')
#    nostim_after = nostim_after.transpose()
#    nostim_after = nostim_after.values
#    
#    nsb=ax[0].boxplot(nostim_before,patch_artist=True, showfliers=False, positions=np.arange(nostim_before.shape[1])-.2, widths=0.3)  
#    sb=ax[0].boxplot(stim_before, patch_artist=True, showfliers=False, positions=np.arange(nostim_before.shape[1])+.2, widths=0.3)
#    
#    nsa=ax[1].boxplot(nostim_after,patch_artist=True, showfliers=False, positions=np.arange(nostim_after.shape[1])-.2, widths=0.3)  
#    sa=ax[1].boxplot(stim_after, patch_artist=True, showfliers=False, positions=np.arange(nostim_after.shape[1])+.2, widths=0.3)
#
#   
#    ax[0].set_xticks(np.arange(len(stim_before[0])))
#    if len(stim_before[1]) > 30:
#        ax[0].set_xticklabels(np.arange(32,81,1))
#    else:
#        ax[0].set_xticklabels(np.arange(1,21,1))
#        
#    ax[0].set_xlim(-0.5,len(stim_before[0])-.5)
#    ax[0].set_ylabel('Power (V/Hz)')
#    ax[0].set_title('Before')
#    
#    
#    ax[1].set_xticks(np.arange(len(stim_before[0])))
#    if len(stim_before[1]) > 30:
#        ax[1].set_xticklabels(np.arange(32,81,1))
#    else:
#        ax[1].set_xticklabels(np.arange(1,21,1))
#        
#    ax[1].set_xlim(-0.5,len(stim_before[0])-.5)
#    ax[1].set_xlabel('Frequency (Hz)')
#    ax[1].set_ylabel('Power (V/Hz)')
#    ax[1].set_title('After')
#   
#    fig.suptitle(stim[file])
##    plt.savefig('D:\F.LARENO.FACCINI\Preliminary Results\Ephy\Power values - Copy\Figures\Stim vs NoStim\Valve\{}.pdf'.format(stim[file]))
#    plt.close()  


##-------------------------- Extracting the MEDIAN ----------------------------

#    nsb_med, sb_med,  nsa_med, sa_med = [], [], [], []
#
#    for medline in nsb['medians']:
#        linedata = medline.get_ydata()
#        median = linedata[0]
#        nsb_med.append(median)
#    for medline in sb['medians']:
#        linedata = medline.get_ydata()
#        median = linedata[0]
#        sb_med.append(median)
#    for medline in nsa['medians']:
#        linedata = medline.get_ydata()
#        median = linedata[0]
#        nsa_med.append(median)
#    for medline in sa['medians']:
#        linedata = medline.get_ydata()
#        median = linedata[0]
#        sa_med.append(median)
#
#        
#    if file == 0:
#        nsbf = pd.DataFrame(nsb_med, index=None, columns=[nostim[file]])
#        sbf = pd.DataFrame(sb_med, index=None, columns=[stim[file]])
#        nsaf = pd.DataFrame(nsa_med, index=None, columns=[nostim[file]])
#        saf = pd.DataFrame(sa_med, index=None, columns=[stim[file]])
#
#    else:
#        nsbf[nostim[file]] = pd.DataFrame(nsb_med, index=None)
#        sbf[stim[file]] = pd.DataFrame(sb_med, index=None)
#        nsaf[nostim[file]] = pd.DataFrame(nsa_med, index=None)
#        saf[stim[file]] = pd.DataFrame(sa_med, index=None)
#
#    save_dir = 'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Power values - Copy/Valve/'
#
#    with pd.ExcelWriter('{}/Median_valve.xlsx'.format(save_dir), engine='openpyxl') as writer:
#                           
#        nsbf.to_excel(writer, sheet_name='NoStim_Before', index=False, header=True)
#        sbf.to_excel(writer, sheet_name='Stim_Before', index=False, header=True)
#        nsaf.to_excel(writer, sheet_name='NoStim_After', index=False, header=True)
#        saf.to_excel(writer, sheet_name='Stim_After', index=False, header=True)


###############################################################################
##-------------------------- Stim vs. No Stim (3 sheets) --------------------##
###############################################################################    
#
#files = glob.glob('D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Power values/rbf with different time windows for control/Fake_P15_Low/*.xlsx')
#names = [os.path.basename(x)  for x in files]
#
#nostim = []
#stim = []
#
##Remove the extension from the name in the list
#
#for x in range(len(names)):
#    names[x] = names[x].replace(".xlsx","")
#    if 'No' in names[x]:
#        nostim.append(names[x])
#    else:
#        stim.append(names[x])
#
#
#for file in range(len(stim)):
#    
#    fig, ax = plt.subplots(3,1, figsize=(15,10))
#   
#    stim_path = 'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Power values/rbf with different time windows for control/Fake_P15_Low/{}.xlsx'.format(stim[file])
#    nostim_path = 'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Power values/rbf with different time windows for control/Fake_P15_Low/{}.xlsx'.format(nostim[file])
#    
#    print(stim_path)
#    print(nostim_path)
#    print('--------------------------------------------------')
#
#    
#    stim_before = pd.read_excel(stim_path, sheet_name='Before (500 ms)')
#    stim_before = stim_before.transpose()
#    stim_before = stim_before.values
#
#    nostim_before = pd.read_excel(nostim_path, sheet_name='Before (500 ms)')
#    nostim_before = nostim_before.transpose()
#    nostim_before = nostim_before.values
#
#    stim_during = pd.read_excel(stim_path, sheet_name='During (500 ms)')
#    stim_during = stim_during.transpose()
#    stim_during = stim_during.values
#    
#    nostim_during = pd.read_excel(nostim_path, sheet_name='During (500 ms)')
#    nostim_during = nostim_during.transpose()
#    nostim_during = nostim_during.values
#
#    
#    stim_after = pd.read_excel(stim_path, sheet_name='After (500 ms)')
#    stim_after = stim_after.transpose()
#    stim_after = stim_after.values
#    
#    nostim_after = pd.read_excel(nostim_path, sheet_name='After (500 ms)')
#    nostim_after = nostim_after.transpose()
#    nostim_after = nostim_after.values
#    
#    nsb = ax[0].boxplot(nostim_before,patch_artist=True, showfliers=False, positions=np.arange(nostim_before.shape[1])-.2, widths=0.3)  
#    sb = ax[0].boxplot(stim_before, patch_artist=True, showfliers=False, positions=np.arange(nostim_before.shape[1])+.2, widths=0.3)
#
#    nsd = ax[1].boxplot(nostim_during,patch_artist=True, showfliers=False, positions=np.arange(nostim_during.shape[1])-.2, widths=0.3)  
#    sd = ax[1].boxplot(stim_during, patch_artist=True, showfliers=False, positions=np.arange(nostim_during.shape[1])+.2, widths=0.3)
#
#    nsa = ax[2].boxplot(nostim_after,patch_artist=True, showfliers=False, positions=np.arange(nostim_after.shape[1])-.2, widths=0.3)  
#    sa = ax[2].boxplot(stim_after, patch_artist=True, showfliers=False, positions=np.arange(nostim_after.shape[1])+.2, widths=0.3)
#
#   
#    
#    ax[0].set_xticks(np.arange(len(stim_before[0])))
#    if len(stim_before[1]) > 30:
#        ax[0].set_xticklabels(np.arange(32,81,1))
#    else:
#        ax[0].set_xticklabels(np.arange(1,21,1))
#        
#    ax[0].set_xlim(-0.5,len(stim_before[0])-.5)
#    ax[0].set_ylabel('Power (V/Hz)')
#    ax[0].set_title('Before')
#    
#    
#    
#    ax[1].set_xticks(np.arange(len(stim_before[0])))
#    if len(stim_before[1]) > 30:
#        ax[1].set_xticklabels(np.arange(32,81,1))
#    else:
#        ax[1].set_xticklabels(np.arange(1,21,1))
#        
#    ax[1].set_xlim(-0.5,len(stim_before[0])-.5)
#    ax[1].set_ylabel('Power (V/Hz)')
#    ax[1].set_title('During')
#
#
#    ax[2].set_xticks(np.arange(len(stim_before[0])))
#    if len(stim_before[1]) > 30:
#        ax[2].set_xticklabels(np.arange(32,81,1))
#    else:
#        ax[2].set_xticklabels(np.arange(1,21,1))
#        
#    ax[2].set_xlim(-0.5,len(stim_before[0])-.5)
#    ax[2].set_xlabel('Frequency (Hz)')
#    ax[2].set_ylabel('Power (V/Hz)')
#    ax[2].set_title('After')
#
#
##    fig.suptitle(stim[file])
##    plt.savefig('D:\F.LARENO.FACCINI\Preliminary Results\Ephy\Power values\Figures\Stim vs NoStim\Second Cue\{}.pdf'.format(stim[file]))
#    plt.close()  
#
#
##-------------------------- Extracting the MEDIAN ----------------------------
#  
#    nsb_med, sb_med, nsd_med, sd_med, nsa_med, sa_med = [], [], [], [], [], []
#
#    for medline in nsb['medians']:
#        linedata = medline.get_ydata()
#        median = linedata[0]
#        nsb_med.append(median)
#    for medline in sb['medians']:
#        linedata = medline.get_ydata()
#        median = linedata[0]
#        sb_med.append(median)
#    for medline in nsd['medians']:
#        linedata = medline.get_ydata()
#        median = linedata[0]
#        nsd_med.append(median)
#    for medline in sd['medians']:
#        linedata = medline.get_ydata()
#        median = linedata[0]
#        sd_med.append(median)
#    for medline in nsa['medians']:
#        linedata = medline.get_ydata()
#        median = linedata[0]
#        nsa_med.append(median)
#    for medline in sa['medians']:
#        linedata = medline.get_ydata()
#        median = linedata[0]
#        sa_med.append(median)
#
#        
#    if file == 0:
#        nsbf = pd.DataFrame(nsb_med, index=None, columns=[nostim[file]])
#        sbf = pd.DataFrame(sb_med, index=None, columns=[stim[file]])
#        nsdf = pd.DataFrame(nsd_med, index=None, columns=[nostim[file]])
#        sdf = pd.DataFrame(sd_med, index=None, columns=[stim[file]])
#        nsaf = pd.DataFrame(nsa_med, index=None, columns=[nostim[file]])
#        saf = pd.DataFrame(sa_med, index=None, columns=[stim[file]])
#
#    else:
#        nsbf[nostim[file]] = pd.DataFrame(nsb_med, index=None)
#        sbf[stim[file]] = pd.DataFrame(sb_med, index=None)
#        nsdf[nostim[file]] = pd.DataFrame(nsd_med, index=None)
#        sdf[stim[file]] = pd.DataFrame(sd_med, index=None)
#        nsaf[nostim[file]] = pd.DataFrame(nsa_med, index=None)
#        saf[stim[file]] = pd.DataFrame(sa_med, index=None)
#
#    save_dir = 'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Power values/rbf with different time windows for control/Fake_P15_Low/'
#
#    with pd.ExcelWriter('{}/Median_lightstim_fakeP15_Low.xlsx'.format(save_dir), engine='openpyxl') as writer:
#                           
#        nsbf.to_excel(writer, sheet_name='NoStim_Before', index=False, header=True)
#        sbf.to_excel(writer, sheet_name='Stim_Before', index=False, header=True)
#        nsdf.to_excel(writer, sheet_name='NoStim_During', index=False, header=True)
#        sdf.to_excel(writer, sheet_name='Stim_During', index=False, header=True)
#        nsaf.to_excel(writer, sheet_name='NoStim_After', index=False, header=True)
#        saf.to_excel(writer, sheet_name='Stim_After', index=False, header=True)
