# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:57:53 2019

@author: Federica LARENO FACCINI (modified from Sam Garcia)
"""

#from compute_timefreq import compute_timefreq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy.signal
from scipy import fftpack
import os
import glob
from collections import OrderedDict
import pandas as pd

'''
In here I am:
    - computing the Morlet Scalogram for each tetrode (channel group) |
    - extracting the power values                                     | --> All of this For each tetrode of each recording, individually 
    - appending these power values in a Excel file                    |
'''



#---------------------------------------!!!!!!!!!! FUNCTIONS !!!!!!!!!!-------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#---------------------------------------------------DO NOT--------------------------------------------------------
#---------------------------------------------------MODIFY--------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#--------------------------------------------GO BELOW FOR DATA INPUT----------------------------------------------
def generate_wavelet_fourier(len_wavelet, f_start, f_stop, delta_freq, 
            sampling_rate, f0, normalisation):
    """
    Compute the wavelet coefficients at all scales and makes its Fourier transform.
    When different signal scalograms are computed with the exact same coefficients, 
        this function can be executed only once and its result passed directly to compute_morlet_scalogram
        
    Output:
        wf : Fourier transform of the wavelet coefficients (after weighting), Fourier frequencies are the first 
    """
    # compute final map scales
    scales = f0/np.arange(f_start,f_stop,delta_freq)*sampling_rate
    # compute wavelet coeffs at all scales
    xi=np.arange(-len_wavelet/2.,len_wavelet/2.)
    xsd = xi[:,np.newaxis] / scales
    wavelet_coefs=np.exp(complex(1j)*2.*np.pi*f0*xsd)*np.exp(-np.power(xsd,2)/2.)

    weighting_function = lambda x: x**(-(1.0+normalisation))
    wavelet_coefs = wavelet_coefs*weighting_function(scales[np.newaxis,:])

    # Transform the wavelet into the Fourier domain
    #~ wf=fft(wavelet_coefs.conj(),axis=0) <- FALSE
    wf=fftpack.fft(wavelet_coefs,axis=0)
    wf=wf.conj() # at this point there was a mistake in the original script
    
    return wf


def convolve_scalogram(sig, wf):
    """
    Convolve with fft the signal (in time domain) with the wavelet
    already computed in freq domain.
    
    Parameters
    ----------
    sig: numpy.ndarray (1D, float)
        The signal
    wf: numpy.array (2D, complex)
        The wavelet coefficient in fourrier domain.
    """
    n = wf.shape[0]
    assert sig.shape[0]<=n, 'the sig.size is longer than wf.shape[0] {} {}'.format(sig.shape[0], wf.shape[0])
    sigf=fftpack.fft(sig,n)
    wt_tmp=fftpack.ifft(sigf[:,np.newaxis]*wf,axis=0)
    wt = fftpack.fftshift(wt_tmp,axes=[0])
    return wt

def compute_timefreq(sig, sampling_rate, f_start, f_stop, delta_freq=1., nb_freq=None,
                f0=2.5,  normalisation = 0.,  min_sampling_rate=None, wf=None,
                t_start=0., zero_pad=True, joblib_memory=None):
    """
    
    """
    #~ print 'compute_timefreq'
    sampling_rate = float(sampling_rate)
    
    if nb_freq is not None:
        delta_freq = (f_stop-f_start)/nb_freq
    
    if min_sampling_rate is None:
        min_sampling_rate =  min(4.* f_stop, sampling_rate)
        
    
    #decimate
    ratio = int(sampling_rate/min_sampling_rate)
    #~ print 'ratio', ratio
    if ratio>1:
        # sig2 = tools.decimate(sig, ratio)
        sig2 = scipy.signal.decimate(sig, ratio, n=4, zero_phase=True)
    else:
        sig2 = sig
        ratio=1
    
    tfr_sampling_rate = sampling_rate/ratio
    #~ print 'tfr_sampling_rate', tfr_sampling_rate
    
    n_init = sig2.size
    if zero_pad:
        n = int(2 ** np.ceil(np.log(n_init)/np.log(2))) # extension to next power of  2
    else:
        n = n_init
    #~ print 'n_init', n_init, 'n', n
    if wf is None:
        if joblib_memory is None:
            func = generate_wavelet_fourier
        else:
            func = joblib_memory.cache(generate_wavelet_fourier)
        wf = func(n, f_start, f_stop, delta_freq, 
                            tfr_sampling_rate, f0, normalisation)
    
    assert wf.shape[0] == n
    
    wt = convolve_scalogram(sig2, wf)
    wt=wt[:n_init,:]
    
    freqs = np.arange(f_start,f_stop,delta_freq)
    times = np.arange(n_init)/tfr_sampling_rate + t_start
    return wt, times, freqs, tfr_sampling_rate


#-------------------------RIDGE EXTRACTION in 2D-------------------------------
#------------------------------------------------------------------------------
def ridge_map(ampl_map, threshold=70.):
    max_power = np.max(ampl_map) #Max power observed in frequency spectrum
    freq_power_threshold = float(threshold) #The threshold range for power detection of the ridge 
    cut_off_power = max_power/100.0*freq_power_threshold #Computes power above trheshold
    
    boolean_map = ampl_map >= cut_off_power #For plot 
    
    value_map = ampl_map
    
    for i,j in np.ndenumerate(ampl_map):
        if j <= cut_off_power:
            value_map[i] = 0.0 #For computation, all freq < trhesh = 0.0
            
    return boolean_map, value_map


#-------------------------SIGNAL FILTERING FUNCTION----------------------------
#------------------------------------------------------------------------------
def filter_signal(signal, order=8, sample_rate=20000,freq_low=400,freq_high=2000, axis=0):
    
    import scipy.signal
    
    Wn = [freq_low/(sample_rate/2),freq_high/(sample_rate/2)]
    
    sos_coeff = scipy.signal.iirfilter(order,Wn,btype='band',ftype='butter',output='sos')
    
    filtered_signal = scipy.signal.sosfiltfilt(sos_coeff, signal, axis=axis)
    
    return filtered_signal

#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':  

    #---------------------------------------------- Signal info : FILL HERE -------------------------------------------
    #------------------------------------------------------------------------------------------------------------------
    
    #Some parameters
    depth = 1350                 
    protocol = 'P20'
    mouse = 858
    state = 'Low'
    location = 'VII'
    
    #Sampling rate (in Hertz) and start time (in seconds) and channel
    sampling_rate= 20000. 
    t_start = 0. 
    
    #Freq window for Morlet Wavelet scalo (in Hz)
    f_start = 1.
    f_stop = 20.
#    f_start = 32
#    f_stop = 80.
    
    #Freq borders for filtered plot (in Hz)
    freq_low=1
    freq_high=100
       
    #Time of light stim
    stim_start = 4
    stim_end = 8

    
    ####### iterate trhough files ######
    
    #Import all the files, by creating a list of them
    files = glob.glob('D:\F.LARENO.FACCINI\Preliminary Results\Ephy\Coordinate Hunting\{}\RBF\{}\{}\*.rbf'.format(mouse,location,protocol))
    names = [os.path.basename(x) for x in files]
    savedir = (r'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Coordinate Hunting/{}/RBF/{}/{}/'.format(mouse,location,protocol))


    
#    cmap = plt.cm.get_cmap('viridis')
    cmap = ['black', 'red', 'blue', 'seagreen', 'gold', 'purple', 'deepskyblue', 'lightsalmon', 'hotpink', 'yellow', 'cyan', 'magenta']
    
    #Remove the extension from the name in the list
    for x in range(len(names)):
        names[x] = names[x].replace(".rbf","")
    
    if len(names) == 0:
        print('This is not the directory you are looking for')
      
    else:
        
        for f in range(len(names)):
    
            print (names[f])
            #loop to iterate the files
           
            #Location of the file
            path ='D:\F.LARENO.FACCINI\Preliminary Results\Ephy\Coordinate Hunting\{}\RBF\{}\{}\{}.rbf'.format(mouse,location,protocol,names[f])
            file = np.fromfile(path, dtype='float64').reshape(-1,16)
            
            ch_group = ([0,2,4,6],[1,3,5,7],[9,11,13,15],[8,10,12,14])
            
            for i in range(len(ch_group)):
                temp__, T= [], []            
                
                for j in range(len(ch_group[i])):
                    temp__.append(np.array(file[:,[ch_group[i][j]]]))
    
                avg = np.mean(temp__, axis=0).ravel()
                T.append(avg)
                    
                
        #--------------------------------------------- THAT'S IT----------------------------------------------------------
        #----------------------------------------------------------------------------------------------------------------- 
                
                #Define the signal, its length in seconds and a time vector
                duration = 1./sampling_rate * len(avg)
                sig_times = np.arange(0, duration, 1./sampling_rate)
                
                if len(sig_times) > len(avg):
                    sig_times = sig_times[:-1]
            
                
                #Fig 1 : the raw signal
                fig, ax = plt.subplots(2,1, sharex=True, figsize=(12,8))
                ax[0].set_title('ch_group %s of %s' %(i,names[f]))
                ax[0].plot(sig_times, avg, linewidth=0.3, label='Raw signal')
                ax[0].plot(sig_times,filter_signal(avg,freq_low=freq_low,freq_high=freq_high), linewidth=0.3,color='orange', label='Filtered signal ({}-{}Hz)'.format(freq_low,freq_high))
                ax[0].set_ylabel('Amplitude (V)')
#                ax[0].axvspan(0, 0.5,color='g', alpha = 0.2)
#                ax[0].axvspan(1.5, 2,color='g', alpha = 0.4)
#                ax[0].axvspan(stim_start, stim_end,color='b', alpha = 0.2)
#                ax[0].axvspan(2.55, 2.7,color='r', alpha = 0.2)
    
    
                #Fig 2 : Timefreq
                ax[1].set_ylabel('Freq (Hz)')
                ax[1].set_xlabel('Time (s)')
                ax[1].set_title('Scalogram')
#                ax[1].axvspan(0, 0.5,color='g', alpha = 0.2)
#                ax[1].axvspan(1.5, 2,color='g', alpha = 0.4)
#                ax[1].axvspan(stim_start, stim_end,color='b', alpha = 0.2)
#                ax[1].axvspan(2.55, 2.7,color='r', alpha = 0.2)

    
                complex_map, map_times, freqs, tfr_sampling_rate = compute_timefreq(avg, sampling_rate, f_start, f_stop, delta_freq=0.1, nb_freq=None,
                                f0=2.5,  normalisation = 0., t_start=t_start)
                
                #print(map_times)
                
                ampl_map = np.abs(complex_map) # the amplitude map (module)
                phase_map = np.angle(complex_map) # the phase
                
                
                delta_freq = freqs[1] - freqs[0]               
                extent = (map_times[0], map_times[-1], freqs[0]-delta_freq/2., freqs[-1]+delta_freq/2.)
                
                scalo = ax[1].imshow(ampl_map.transpose(), interpolation='nearest', 
                                    origin ='lower', aspect = 'auto', extent = extent, cmap='viridis')
    
                ax[0].legend()
#                fig.colorbar(scalo)
                plt.savefig(savedir + '{}_ChGroup{}_{}.pdf'.format(names[f], i,state))
                plt.close()
        
        #---------------------- Extracting power values --------------------------------
        
                start_before = int(1.*tfr_sampling_rate)
                end_before = int(1.5*tfr_sampling_rate)
                start_during = int(1.8*tfr_sampling_rate)
                end_during = int(2.3*tfr_sampling_rate)
                start_after = int(2.3*tfr_sampling_rate)
                end_after = int(2.8*tfr_sampling_rate)
                
                before = ampl_map.transpose()[:,start_before:end_before]
                during = ampl_map.transpose()[:,start_during:end_during]
                after = ampl_map.transpose()[:,start_after:end_after]
        
                avg_before = np.true_divide(before.sum(1),(before!=0).sum(1))
                avg_during = np.true_divide(during.sum(1),(during!=0).sum(1))
                avg_after = np.true_divide(after.sum(1),(after!=0).sum(1))
                
#                print(after.shape)
#                print(len(avg_after))
        #------------------------ Writing to the Excel file ---------------------------
#    #            print(names[f],i)
#                  
#                a = np.vstack((avg_before))#.transpose()
##                b = np.vstack((avg_during))#.transpose()
##                c = np.vstack((avg_after))#.transpose()
#                
#                if f+i==0: 
#                    df1 = pd.DataFrame(a,columns=['%s_%s'%(names[f],i)])
##                    df2 = pd.DataFrame(b,columns=['%s_%s'%(names[f],i)])
##                    df3 = pd.DataFrame(c,columns=['%s_%s'%(names[f],i)])
#    
#                else:                
#                    df1['%s_%s'%(names[f],i)] = a
##                    df2['%s_%s'%(names[f],i)] = b
##                    df3['%s_%s'%(names[f],i)] = c
#    
#    
#                powerdir = (r'D:/F.LARENO.FACCINI/Preliminary Results/Ephy/Bands')
#                  
##                with pd.ExcelWriter('{}/{}_power_values_valve_{}_NoStim_{}.xlsx'.format(powerdir,mouse,protocol,state), engine='openpyxl') as writer:
#                with pd.ExcelWriter('{}/average_band.xlsx'.format(powerdir), engine='openpyxl') as writer:
#                    df1.to_excel(writer, sheet_name='Before (500 ms)')
##                    df2.to_excel(writer, sheet_name='During (500 ms)')
##                    df3.to_excel(writer, sheet_name='After (500 ms)')
#    
