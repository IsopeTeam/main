# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 15:43:25 2021

@author: Master5.INCI-NSN
"""
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import extrapy.Behaviour as B
import numpy as np

def raster_PSTH_plot_maker(donnees, title, reward_time):
    fig, ax = plt.subplots(2, 1, sharex=True)
    fig.suptitle(title,weight='bold') #main figure title
    
    
    #first subplot (Raster)
    B.scatter_lick(donnees, ax[0], x_label=None)
    ax[0].set_title('RASTER') #Raster subplot title
    
    #second subplot (PSTH)
    B.psth_lick(donnees, ax[1]) #PSTH graph 
    ax[1].set_ylabel('nb of occurence') #PSTH title
    ax[1].set_xlabel('Time') #PSTH x label
    ax[1].set_title('PSTH') #PSTH y label
    
    current_reward_time=2.05+(float(reward_time)/1000) #determine when the reward happen depending of the keys of the dictionary
    ax = ax.ravel()
    for subplot in ax:
        subplot.axvspan(0,0.5, facecolor="green", alpha=0.3)
        subplot.axvspan(1.5,2, facecolor="green", alpha=0.3)
        subplot.axvspan(current_reward_time,current_reward_time+0.15, facecolor="red", alpha=0.3)

def graphique_fixe(lick_file_path):
    donnees = B.load_lickfile(lick_file_path)
    
    raster_PSTH_plot_maker(donnees, 'Fixe delay', 500)

def graphique_random(param_file_path, lick_file_path, dic_graph_choice):
    
    random_delay=B.extract_random_delay(param_file_path)
    lick=B.load_lickfile(lick_file_path)
    delays, licks_by_delay = B.separate_by_delay(random_delay, lick)
    
    for cle,donnees in licks_by_delay.items():
        if dic_graph_choice[cle]:     
            
            raster_PSTH_plot_maker(donnees, cle, cle[-3:])

        else:
            pass
        
sg.theme('DarkBlue')	

layout= [  [sg.Text('Enter .lick File name     '), sg.InputText(), sg.FileBrowse()],
            [sg.Text('Enter .param File name     '), sg.InputText(), sg.FileBrowse()],
            [sg.Radio('Random delay', 'radio_delay', key='radio_random', default=True), sg.Radio('fixe delay', 'radio_delay', key='radio_fixe')],
            [sg.Frame(layout=[      
            [sg.Checkbox('400', default=True), sg.Checkbox('400_400', default=True), \
            sg.Checkbox('900_400', default=True), sg.Checkbox('400_400_400', default=True), \
            sg.Checkbox('900_400_400', default=True)],[sg.Checkbox('900', default=True), \
            sg.Checkbox('900_900', default=True), sg.Checkbox('400_900', default=True), sg.Checkbox('900_900_900', default=True), \
            sg.Checkbox('400_900_900', default=True)]], title='Graph to display',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Last number is the current reward time')],  
            [sg.Button('Display Raster and PSTH plot', key='-Raster PSTH-')]]

"""
values[0]= .lick file path ; values[1]= .param file path ; values[2]= graph 400 ; values[3]= graph 400_400
values[4]= graph 900_400 ; values[5]= graph 400_400_400 ; values[6]= graph 900_400_400 ; values[7]= graph 900 ;
values[8]= graph 900_900 ; values[9]= graph 400_900 ; values[10]= graph 900_900_900 ; values[11]= graph 400_900_900                                                    
"""                                                       
window= sg.Window('Load files', layout, location=(0,0))

while True:
    event, values = window.read()

    try:
        if event in (None, 'Close'):	# if user closes window or clicks cancel
            break
             
        if event == '-Raster PSTH-': 
            if values['radio_random']:   #If we chose to random delay
                if len(values[0])>0 and len(values[1])>0:
                    dic_graph_choice = {"400":values[2],"400_400":values[3],"900_400":values[4],\
                                                    "400_400_400":values[5],"900_400_400":values[6],"900":values[7],\
                                                    "900_900":values[8],"400_900":values[9],"900_900_900":values[10],"400_900_900":values[11]}
                    if values[0][-4:] != 'lick' or values[1][-5:] != 'param':
                        if sg.popup_yes_no('wrong extention, continue anyway?')=='Yes':
                            graphique_random(values[1], values[0], dic_graph_choice)
                            pass
                    else:
                        graphique_random(values[1], values[0], dic_graph_choice)

                else:
                    sg.popup_error('')
                    pass   
        
            if values['radio_fixe']:   #if we chose fixe delay
                if len(values[0])>0 :
                    
                    if values[0][-4:] != 'lick':
                        if sg.popup_yes_no('wrong extention, continue anyway?')=='Yes':
                            graphique_fixe(values[0])
                            pass
                    else:
                        graphique_fixe(values[0])

                else:
                    sg.popup_error('')
                    pass   
        
    except:
        pass
    
window.close()

    