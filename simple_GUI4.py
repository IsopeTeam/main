
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:14:30 2020

@author: Phippe.ISOPE
"""
from matplotlib.backend_bases import MouseButton
import PySimpleGUI as sg
import glob
import os
import neo
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
import pandas as pd


TIME, REC, Saved_REC,Saved_REC2,Subtracted_REC, pos = [],[],[],[],[],[]
AMP, AMP1, AMP2, AMP3 = [], [], [], []
#startpos, endpos = [],[]

###############################
## DEF GET COORDINATE CURSORS #
###############################

def on_click(event):
    global startpos, endpos
    if event.button is MouseButton.LEFT:
        startpos=[event.xdata]
    elif event.button is MouseButton.RIGHT:
        endpos=[event.xdata]
     
#############################
### FIT
#############################    
def Fit_single_trace(Trace, Time_trace):
    
    idx_start=np.ravel(np.where(Time_trace >=startpos[0]))[0]
    idx_stop=np.ravel(np.where(Time_trace >= endpos[0]))[0]
    x = Time_trace[idx_start:idx_stop]
    y = Trace[idx_start:idx_stop]
    x2=np.array(np.squeeze(x))
    y2=np.array(np.squeeze(y))  

    fig_ft=plt.figure()
    ax_fit = fig_ft.add_subplot(111)
    ax_fit.plot(x2,y2,color = 'black', alpha = 1, lw = '1')
     
    param_bounds=([-np.inf,0.,0.,-1000.],[np.inf,1.,1.,1000.])   
    # be careful ok for seconds. If millisec change param 2 and 3
    popt, pcov = curve_fit(func_mono_exp, x2, y2,bounds=param_bounds) 

    ax_fit.plot(x, func_mono_exp(x2, *popt), color = 'red', alpha = 1, lw = '2')
   
    for i in range(10):
        print('iteration:',i)
        p0=(popt[0],popt[1],popt[2], popt[3])
        popt, pcov = curve_fit(func_mono_exp, x2, y2,p0)
        ax_fit.plot(x, func_mono_exp(x2, *popt), color = 'red', alpha = 1, lw = '2')
        
    print ('a * np.exp(-(x-b)/c) + d', popt)
    print ('tau decay =',popt[2]*1000, ' ms' )

def func_mono_exp(x, a, b, c, d):
    return a * np.exp(-(x-b)/c) + d

#def func_line(x, a, b):
#    return a * x + b    
#
#def func_dbl_exp(x, a, b, c, d, e):
#    return a * np.exp(-x/b) + c * np.exp(-x/d)+e
#
#def func_lognormal(x, a, b, c, d):    
#    pass
    
###############################
### DEF LOAD FILE  ############
###############################

def load_wcp(file_wcp):
    my_file = neo.io.WinWcpIO(file_wcp)
    bl = my_file.read_block()
    for episode in bl.segments :
        time = episode.analogsignals[0].times #The time vector
        TIME.append(time)
        rec = episode.analogsignals[0].magnitude#The signal vector 
        REC.append(rec)  #  -leak) #We extract the signal minus the offset
    global sampling
    sampling=float(TIME[1][1])*1000  #sampling rate in ms
        
def load_folder(path):
    list_file=glob.glob(os.path.join(path, '*.wcp'))
    print (list_file)
    for i in range(len(list_file)):
       load_wcp(list_file[i])
  
###############################
### DEF AVERAGE  ############
###############################

def Make_average(REC,TIME,CursorOn):
            
            global AVERAGE
            TAGREC=[]
            for i in range(len(REC)):
                if TAG[i]==1:
                    TAGREC.append(REC[i])
            AVERAGE = np.mean(TAGREC,axis = 0)
            if CursorOn == True:
                min_avg=calc_min_in_trace(AVERAGE, startpos[0], endpos[0], 5)
                max_avg=calc_max_in_trace(AVERAGE, startpos[0], endpos[0], 5)
            
            fig2 = plt.figure()
            ax2 = fig2.add_subplot(111)
            ax2.plot(TIME[0], AVERAGE)
            plt.xlabel('Time (s)')
            plt.ylabel('Signal (Amp)')
            plt.draw()
            if CursorOn == True:
                plt.title('Average: min = '+str(min_avg)+'   max = '+str(max_avg)+'    (Close me)',fontweight="bold", fontsize=12, color="g")
            else:
                plt.title('Average (CLOSE ME)')
#

##########################
# DEF Mode superimposed ##
##########################

def superimposed(episode):
    
    sg.theme('Black')	
 
    layout2 = [ [sg.Text('Superimposed Episodes')],
                [sg.Button('Start'), sg.Button('Close', button_color=('red', 'white'))],
                [sg.Button('Previous Trace'),sg.Button('Next Trace'),sg.Button('Clear')],
                [sg.Text('Go To (Push start)'), sg.InputText(default_text="0", size=(10, 1))]]
    
    window2 = sg.Window('Display Superimposed Traces', layout2, location=(0,600))
    episode = episode
    
    while True:
        
        event2, values2 = window2.read()
        try:
           
            if event2 in (None, 'Close'):	# if user closes window or clicks cancel
                break
    
            if event2 == "Next Trace":
                episode+=1
                ax.plot(TIME[episode], REC[episode])
                plt.xlabel('Time (s)')
                plt.ylabel('Signal (Amp)')
                plt.title('Episode: '+str(episode))
                plt.draw()
     
            if event2 == "Previous Trace":
                episode-=1
                ax.plot(TIME[episode], REC[episode])
                plt.xlabel('Time (s)')
                plt.ylabel('Signal (Amp)')
                plt.title('Episode: '+str(episode))
                plt.draw()
     
            if event2 == "Start":
                ax.clear()
                try:
                    episode=int(values2[0])
                except:
                    episode=0
                ax.plot(TIME[episode], REC[episode])
                plt.xlabel('Time (s)')
                plt.ylabel('Signal (Amp)')
                plt.title('Episode: '+str(episode))
                plt.draw()
    
            if event2 == "Clear":
                ax.clear()
                               

        except:
            sg.popup_error('')
            pass
   
    window2.close()


    
##############################
## FUNCTIONS TO CALCULATE AMPLITUDES ##
##############################    
    
def calc_min_in_trace(trace, win1, win2, Win_for_extremum):
    start_idx = np.ravel(np.where(TIME[0] >= win1))[0]
    stop_idx = np.ravel(np.where(TIME[0] >= win2))[0]
    MIN = np.min(trace[start_idx:stop_idx])
    sub_trace=trace[start_idx:stop_idx]
    MIN_index = np.argmin(sub_trace)
    MIN = np.mean(sub_trace[MIN_index-Win_for_extremum:MIN_index+Win_for_extremum])
    return MIN

def calc_max_in_trace(trace, win1, win2, Win_for_extremum):
    start_idx = np.ravel(np.where(TIME[0] >= win1))[0]
    stop_idx = np.ravel(np.where(TIME[0] >= win2))[0]
    MAX = np.max(trace[start_idx:stop_idx])
    sub_trace=trace[start_idx:stop_idx]
    MAX_index = np.argmax(sub_trace)
    MAX = np.mean(sub_trace[MAX_index-Win_for_extremum:MAX_index+Win_for_extremum])
    return MAX

def Calc_amps_in_trains():
    pass
    sg.theme('Black')	
 
    layout4 = [  [sg.Text('Calculate Amplitudes on Tagged traces')],
                [sg.Checkbox('Minimum', size=(12, 1), default=True)],
                [sg.Text('Win 1 Start'), sg.InputText(default_text="0.1", size=(10, 1))],
                [sg.Text('Win 1 Stop'), sg.InputText(default_text="0.2", size=(10, 1))],
                [sg.Text('Win 2 Start'), sg.InputText(default_text="0.2", size=(10, 1))],
                [sg.Text('Win 2 Stop'), sg.InputText(default_text="0.3", size=(10, 1))],
                [sg.Text('Win 3 Start'), sg.InputText(default_text="0.3", size=(10, 1))],
                [sg.Text('Win 3 Stop'), sg.InputText(default_text="0.4", size=(10, 1))],
                [sg.Button('From values')],
                [sg.Button('From Train')],
                [sg.Text('Calculate Amplitudes on Tagged traces'),sg.InputText(default_text="Amplitudes", size=(10, 1))],
                [sg.Button('Close_Amp', button_color=('red', 'white'))]]
    window4 = sg.Window('Amplitudes', layout4)
#    AMP, AMP1, AMP2, AMP3 = [], [], [], []   
    
    while True:
        
        event4, values4 = window4.read()
        try:
            if event4 in (None, 'Close_Amp'):	# if user closes window or clicks cancel
                break
        
        except:
            sg.popup_error('Tagged traces or cursors missing')
            pass
    window4.close()

def Calculate_Amps():
    
    sg.theme('Black')	
 
    layout3 = [  [sg.Text('Calculate Amplitudes on Tagged traces')],
                [sg.Checkbox('Minimum', size=(12, 1), default=True)],  
                [sg.Button('From Cursors')],
                [sg.Button('From values')],
                [sg.Text('Win 1 Start'), sg.InputText(default_text="0.1", size=(10, 1))],
                [sg.Text('Win 1 Stop'), sg.InputText(default_text="0.2", size=(10, 1))],
                [sg.Text('Win 2 Start'), sg.InputText(default_text="0.2", size=(10, 1))],
                [sg.Text('Win 2 Stop'), sg.InputText(default_text="0.3", size=(10, 1))],
                [sg.Text('Win 3 Start'), sg.InputText(default_text="0.3", size=(10, 1))],
                [sg.Text('Win 3 Stop'), sg.InputText(default_text="0.4", size=(10, 1))],
                [sg.Text('Number of Points (+/-)'), sg.InputText(default_text="5", size=(10, 1))],
                [sg.Button('From Train')],
                [sg.Text('Save as'),sg.InputText(default_text="Amplitudes", size=(10, 1))],
                [sg.Text('')],
                [sg.Button('Close_Amp', button_color=('black', 'white'))]]
    
    window3 = sg.Window('Amplitudes', layout3, location=(900,0))
       
    while True:
        
        event3, values3 = window3.read()
        try:
           
            if event3 in (None, 'Close_Amp'):	# if user closes window or clicks cancel
                break
            
            if event3 == "From Cursors":
                AMP = []
                for i in range(len(REC)):
                    if values3[0] == True:
                        if TAG[i] == 1:
                            AMP.append(calc_min_in_trace(REC[i], startpos[0], endpos[0],int(values3[7])))
                    else:
                        if TAG[i] == 1:
                            AMP.append(calc_max_in_trace(REC[i], startpos[0], endpos[0], int(values3[7])))
 
                fig4 = plt.figure()
                ax4 = fig4.add_subplot(111)
                ax4.plot(AMP)
                plt.xlabel('Number episodes')
                plt.ylabel('Signal (Amp)')
                plt.title('Amplitude Timecourse')
                data = {'Amp': np.array(AMP)}
                df = pd.DataFrame.from_dict(data)
                writer = pd.ExcelWriter(str(values3[8])+'.xlsx')
                df.to_excel(writer)
                writer.save() 
                
            if event3 == "From values":
                AMP1, AMP2, AMP3 = [], [], []
                for i in range(len(REC)):
                    if values3[0] == True:
                        if TAG[i] == 1:
                            AMP1.append(calc_min_in_trace(REC[i],float(values3[1]),float(values3[2]),int(values3[7])))
                            AMP2.append(calc_min_in_trace(REC[i],float(values3[3]),float(values3[4]),int(values3[7])))
                            AMP3.append(calc_min_in_trace(REC[i],float(values3[5]),float(values3[6]),int(values3[7])))
                    else:
                        if TAG[i] == 1:
                            AMP1.append(calc_max_in_trace(REC[i],float(values3[1]),float(values3[2]),int(values3[7])))
                            AMP2.append(calc_max_in_trace(REC[i],float(values3[3]),float(values3[4]),int(values3[7])))
                            AMP3.append(calc_max_in_trace(REC[i],float(values3[5]),float(values3[6]),int(values3[7])))
                                 
                fig4 = plt.figure()
                ax4 = fig4.add_subplot(111)
                ax4.plot(AMP1, label = 'Amp1')
                ax4.plot(AMP2, label = 'Amp2')
                ax4.plot(AMP3, label = 'Amp3')
                ax4.legend()
                plt.xlabel('Number episodes')
                plt.ylabel('Signal (Amp)')
                plt.title('Amplitude Timecourse')    
                
                data = {'AMP1': np.array(AMP1), 'AMP2': np.array(AMP2), 'AMP3': np.array(AMP3)}
                df = pd.DataFrame.from_dict(data)
                writer = pd.ExcelWriter(str(values3[8])+'.xlsx')
                df.to_excel(writer)
                writer.save()
                
            if event3 == "From Trains":
                Calc_amps_in_trains()
           
        except:
            sg.popup_error('Tagged traces or cursors missing')
            pass
    window3.close()

 

###########################
## MAIN SCRIPT   ##########
###########################
    
###########################
##   lOAD FILE WINDOW  ####
###########################

sg.theme('DarkBlue')	
layout0= [  [sg.Text('Enter File name'), sg.InputText(), sg.FileBrowse()],
            [sg.Button('Start File')],
            [sg.Text('Enter Folder name'), sg.InputText(), sg.FolderBrowse()],
            [sg.Button('Start Folder')]]
window0= sg.Window('Load files', layout0, location=(0,0))

while True:
    event0, values0 = window0.read()

    try:
               
        if event0 == 'Start File':
            load_wcp(values0[0]) 
            break
        if event0 == 'Start Folder':
            load_folder(values0[1])
            break
    except:
        pass
    
window0.close()    

#############################
#### MAIN WINDOW  ###########
#############################


sg.theme('SandyBeach')	

layout1 = [ [sg.Button('Start'),sg.Button('Previous Trace'),sg.Button('Next Trace'),sg.Button('Clear'),sg.Button('Superimposed'),sg.Text('Go To (Push start)'), sg.InputText(default_text="0", size=(10, 1))],
            [sg.Text('_'*30)],
            [sg.Button('Leak Subtraction'), sg.Text('Window (ms)'),sg.InputText(default_text="0", size=(10, 1)),sg.InputText(default_text="10", size=(10, 1)),sg.Button('Undo leak subtraction')],
            [sg.Text('_'*30)],
            [sg.Button('Smooth Traces'),sg.Text('Odd number'), sg.InputText(default_text="19", size=(10, 1)),sg.Button('Undo Smoothing') ],
            [sg.Text('_'*30)],
            [sg.Button('Tag'), sg.Button('UnTag'), sg.Button('Tag All'), sg.Button('UnTag All'), sg.Button('Save Tags')],
            [sg.Button('Averaged Tagged Traces'),sg.Checkbox('calc on cursors', size=(12, 1), default=False), sg.Button("Save Average"), sg.InputText(default_text="Avg", size=(10, 1))],
            [sg.Text('_'*30)],
            [sg.Button('Select Cursors'),sg.Button('Draw Cursors'),sg.Text('Left/right click: Left/right cursor')],
            [sg.Text('_'*30)],
            [sg.Button('Calculate Amps')],
            [sg.Text('_'*30)],
            [sg.Button('Fit current trace'),sg.Button('Fit all traces'), sg.Button('Fit average')]]


window1 = sg.Window('Browse Traces', layout1, location=(0,0))

episode=0

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

TAG = np.zeros(len(REC))

while True:
    
    event, values = window1.read()
    
    try:
       
        if event in (None, 'Close'):	# if user closes window or clicks cancel
            break
        
        if event == "Superimposed":
            ax.plot(TIME[episode], REC[episode])
            plt.xlabel('Time (s)')
            plt.ylabel('Signal (Amp)')
            plt.title('Episode: '+str(episode))
            superimposed(episode)

        if event == "Leak Subtraction": 
            for i in range(len(REC)):
                Saved_REC2.append(REC[i])
            for i in range(len(REC)):
                rec = REC[i]
                leak = np.mean(rec[int(float(values[1])/sampling):int(float(values[2])/sampling)])
                REC[i]=REC[i]-leak 
           
        if event == "Smooth Traces": 
            for i in range(len(REC)):
                Saved_REC.append(REC[i])
            for i in range(len(REC)):
                REC[i] = savgol_filter(np.squeeze(REC[i]), int(values[3]), 2) # Filter: window size 19, polynomial order 2   
         
        if event == "Undo Smoothing": 
            for i in range(len(REC)):
                REC[i]=Saved_REC[i]


                
        if event == "Undo leak subtraction": 
            for i in range(len(REC)):
                REC[i]=Saved_REC2[i]
           
        if event == "Next Trace":
            ax.clear()
            episode+=1
            if TAG[episode] == 1:
                ax.plot(TIME[episode], REC[episode], color ='r')
            else:
                ax.plot(TIME[episode], REC[episode])
            plt.xlabel('Time (s)')
            plt.ylabel('Signal (Amp)')
            plt.title('Episode '+str(episode), fontweight="bold", fontsize=16, color="g")
            plt.draw()
 
        if event == "Previous Trace":
            ax.clear()
            episode-=1  
            if TAG[episode] == 1:
                ax.plot(TIME[episode], REC[episode], color ='r')
            else:
                ax.plot(TIME[episode], REC[episode])
            plt.xlabel('Time (s)')
            plt.ylabel('Signal (Amp)')
            plt.title('Episode '+str(episode), fontweight="bold", fontsize=16, color="g")
            plt.draw()
                       
        if event == "Start":
            ax.clear()
            try:
                episode=int(values[0])
            except:
                episode=0
            if TAG[episode] == 1:    
                ax.plot(TIME[episode], REC[episode], color ='r')
            else:
                ax.plot(TIME[episode], REC[episode])
            plt.xlabel('Time (s)')
            plt.ylabel('Signal (Amp)')
            plt.title('Episode '+str(episode), fontweight="bold", fontsize=16, color="g")
            plt.draw()

        if event == "Clear":
            ax.clear()
            plt.draw()
            
        if event == "Tag":
            TAG[episode]=1
 
        if event == "UnTag":
            TAG[episode]=0
  
        if event == "Tag All":
            TAG= [1 for i in range(len(REC))]
       
        if event == "UnTag All":
            TAG= [0 for i in range(len(REC))]   

        if event == "Save Tags":
            df = pd.DataFrame(TAG, columns=['Tags'])
            writer = pd.ExcelWriter('Tags.xlsx')
            df.to_excel(writer, index = False)
            writer.save()
                        
        if event == "Averaged Tagged Traces":
            Make_average(REC,TIME,values[4])
        
        if event == "Save Average":
            df = pd.DataFrame(AVERAGE, columns=['Average'])
            writer = pd.ExcelWriter(str(values[5])+'.xlsx')
            df.to_excel(writer, index = False)
            writer.save()

                
        if event == 'Select Cursors': 
            cid=fig.canvas.mpl_connect('button_press_event', on_click)
                              
        if event == 'Draw Cursors': 
            fig.canvas.mpl_disconnect(cid)
            try:
                ax.axvline(startpos[0], color ='r')
                ax.axvline(endpos[0], color ='g')
                fig.canvas.draw()
            except:
                pass
            
        if event == 'Calculate Amps':
            Calculate_Amps()
            
        if event == 'Fit current trace':    
            Fit_single_trace(REC[episode], TIME[episode])
            
        if event == 'Fit all traces':    
            Fit_single_trace(REC[episode], TIME[episode])
            
        if event == 'Fit average':    
            Fit_single_trace(REC[episode], TIME[episode])    
        
            
    except:
        sg.popup_error('')
        pass
        
window1.close()



    
    
    

    
