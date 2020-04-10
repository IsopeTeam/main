# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:14:30 2020

@author: Phippe.ISOPE
"""

import PySimpleGUI as sg
import neo
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter
import pandas as pd

TIME, REC = [],[]
pos = []


def load_wcp(file_wcp):
    my_file = neo.io.WinWcpIO(file_wcp)
    bl = my_file.read_block()
    for episode in bl.segments :
        time = episode.analogsignals[0].times #The time vector
        TIME.append(time)
        rec = episode.analogsignals[0].magnitude#The signal vector 
        rec = savgol_filter(np.squeeze(rec), 19, 2) # Filter: window size 19, polynomial order 2   
        leak = np.mean(rec[0:100]) #The offest of the trace
        REC.append(rec-leak) #We extract the signal minus the offset
     
def onclick(event):
    pos.append([event.xdata,event.ydata])
#    cursor=pos[0]
#    ax.axvline(cursor[0], color ='r')  
    
############################"
##   WINDOW 1: LOAD FILE: REC is the matrix with all the traces
###########################

sg.theme('DarkAmber')	
layout = [  [sg.Text('Enter File name'), sg.InputText(), sg.FileBrowse()],
            [sg.Button('Start')]]
window = sg.Window('Load files', layout)
while True:
    event, values = window.read()
    try:
        load_wcp(values[0]) 
        break
    except:
        pass
window.close()    

#############################
#### WINDOW 2: START DISPLAY TRACE
##############################


sg.theme('DarkAmber')	
# All the stuff inside your window.
layout1 = [  [sg.Text('Display Episodes')],
            [sg.Button('Start'), sg.Button('Close'),sg.Button('Previous Trace'),sg.Button('Next Trace'),sg.Button('Clear'),sg.Button('Superimposed'),sg.Text('Go To (Push start)'), sg.InputText(size=(10, 1))],
            [sg.Text('Select Traces')],
            [sg.Button('Tag'), sg.Button('UnTag'), sg.Button('Tag All'), sg.Button('UnTag All')],
            [sg.Text('Analysis')],
            [sg.Button('Averaged Tagged Traces'),sg.Button('Save as ***.xls'),sg.InputText(size=(10, 1))],
            [sg.Text('Define Cursors')],
            [sg.Button('Start Cursor'),sg.Button('Stop Cursor'),sg.Button('Draw Cursors'),sg.Text('Dble click on the fig then push Start or Stop, then Draw')],
            [sg.Button('Calculate Amps')]]


window1 = sg.Window('Display Traces', layout1)

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
            ax.plot(TIME[1], REC[episode])
            plt.xlabel('Time (s)')
            plt.ylabel('Signal (Amp)')
            plt.title('Episode: '+str(episode))
            superimposed()
            
        if event == "Next Trace":
            ax.clear()
            episode+=1
            if TAG[episode] == 1:
                ax.plot(TIME[1], REC[episode], color ='r')
            else:
                ax.plot(TIME[1], REC[episode])
            print(episode)
            plt.xlabel('Time (s)')
            plt.ylabel('Signal (Amp)')
            plt.title('Episode: '+str(episode))
            plt.draw()
#            episode+=1
 
        if event == "Previous Trace":
            ax.clear()
            episode-=1  
            if TAG[episode] == 1:
                ax.plot(TIME[1], REC[episode], color ='r')
            else:
                ax.plot(TIME[1], REC[episode])
            print (episode)
            plt.xlabel('Time (s)')
            plt.ylabel('Signal (Amp)')
            plt.title('Episode: '+str(episode))
            plt.draw()
 #           episode-=1  
            
        if event == "Start":
            ax.clear()
            try:
                episode=int(values[0])
            except:
                episode=0
            if TAG[episode] == 1:    
                ax.plot(TIME[1], REC[episode], color ='r')
            else:
                ax.plot(TIME[1], REC[episode])
            print(episode)
            plt.xlabel('Time (s)')
            plt.ylabel('Signal (Amp)')
            plt.title('Episode: '+str(episode))
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
        
        if event == "Averaged Tagged Traces":
            TAGREC=[]
            for i in range(len(REC)):
                if TAG[i]==1:
                    TAGREC.append(REC[i])
            AVERAGE = np.mean(TAGREC,axis = 0)
            fig2 = plt.figure()
            ax2 = fig2.add_subplot(111)
            ax2.plot(TIME[1], AVERAGE)
            plt.xlabel('Time (s)')
            plt.ylabel('Signal (Amp)')
            plt.title('Average (CLOSE ME)')
        
        if event == 'Save as ***.xls': 
            df = pd.DataFrame(AVERAGE, columns=['Average'])
            print (df)
            writer = pd.ExcelWriter(str(values[1])+'.xlsx')
            df.to_excel(writer, index = False)
            writer.save()
            
        if event == 'Start Cursor': 
            fig.canvas.mpl_connect('button_press_event', onclick)
            Start_Cursor=pos[-1]
#            pos=[]
        if event == 'Stop Cursor': 
            fig.canvas.mpl_connect('button_press_event', onclick)
            Stop_Cursor=pos[-1]
#            pos=[]

        if event == 'Draw Cursors': 
            try:
                ax.axvline(Start_Cursor[0], color ='r')
                ax.axvline(Stop_Cursor[0], color ='g')
                fig.canvas.draw()
            except:
                pass
        if event == 'Calculate Amps':
            Calculate_Amps()
            
            
    except:
        pass
        
window1.close()


##########################
#Mode superimposed
##########################""""

def superimposed():
    
    sg.theme('Dark Green 5')	
 
    layout2 = [  [sg.Text('Superimposed Episodes')],
                [sg.Button('Start'), sg.Button('Close')],
                [sg.Button('Previous Trace'),sg.Button('Next Trace'),sg.Button('Clear')],
                [sg.Text('Go To (Push start)'), sg.InputText(size=(10, 1))]]
    
    window2 = sg.Window('Display Superimposed Traces', layout2)
       
    while True:
        
        event2, values2 = window2.read()
        try:
           
            if event2 in (None, 'Close'):	# if user closes window or clicks cancel
                break
    
            if event2 == "Next Trace":
                episode+=1
                ax.plot(TIME[1], REC[episode])
                plt.xlabel('Time (s)')
                plt.ylabel('Signal (Amp)')
                plt.title('Episode: '+str(episode))
                plt.draw()
     
            if event2 == "Previous Trace":
                episode-=1
                ax.plot(TIME[1], REC[episode])
                plt.xlabel('Time (s)')
                plt.ylabel('Signal (Amp)')
                plt.title('Episode: '+str(episode))
                plt.draw()
     
            if event2 == "Start":
                ax.clear()
                try:
                    episode=int(values2[1])
                except:
                    episode=0
                ax.plot(TIME[1], REC[episode])
                plt.xlabel('Time (s)')
                plt.ylabel('Signal (Amp)')
                plt.title('Episode: '+str(episode))
                plt.draw()
    
            if event2 == "Clear":
                ax.clear()
                               

        except:
            pass
    window2.close()
    
    
    
##################################
##CALCULATE AMPS
################################
    
def Calculate_Amps():
    
    sg.theme('Black')	
 
    layout3 = [  [sg.Text('Calculate Amplitudes')],
                [sg.Button('From Cursors')],
                [sg.Checkbox('Minimum', size=(12, 1), default=True)],
                [sg.Text('Win 1 Start'), sg.InputText(size=(10, 1))],
                [sg.Text('Win 1 Stop'), sg.InputText(size=(10, 1))],
                [sg.Text('Win 2 Start'), sg.InputText(size=(10, 1))],
                [sg.Text('Win 2 Stop'), sg.InputText(size=(10, 1))],
                [sg.Text('Win 3 Start'), sg.InputText(size=(10, 1))],
                [sg.Text('Win 3 Stop'), sg.InputText(size=(10, 1))],
                [sg.Button('From values')],
                [sg.Button('Close_Amp')] ]
    
    window3 = sg.Window('Amplitudes', layout3)
       
    while True:
        
        event3, values3 = window3.read()
        try:
           
            if event3 in (None, 'Close_Amp'):	# if user closes window or clicks cancel
                break
            
            if event3 == "From Cursors":
                AMP = []
                print (event3,values3)
                for i in range(len(REC)):
                    if values3[0] == True:
                        print ('yes')
                        if TAG[i] == 1:
#                            start = np.ravel(np.where(TIME[0] >= Start_Cursor[0]))[0]
#                            stop = np.ravel(np.where(TIME[0] >= Stop_Cursor[0]))[0]

                            MIN_EPISODE = np.min(REC[i][Start_Cursor[0]:Stop_Cursor[0]])
                            AMP.append(MIN_EPISODE)
                    else:
                        if TAG[i] == 1:
                            MAX_EPISODE = np.max(REC[i][Start_Cursor[0]:Stop_Cursor[0]])
                            AMP.append(MAX_EPISODE)
                print (AMP)
                ax.plot(AMP)
                plt.xlabel('Episode number')
                plt.ylabel('Amp)')
                plt.title('Timecourse')
                plt.draw()
    
            if event3 == "From values":
                pass
                                 

        except:
            pass
    window3.close()
