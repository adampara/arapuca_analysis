
# coding: utf-8

# ##### import files
# select single pe signals for a templete

# In[1]:

import matplotlib.pyplot as plt
from ROOT import gRandom, TCanvas, TH1F, TFile, TTree,TH2F,gDirectory, TF1,TF2,gStyle, TBrowser, gSystem
import ROOT
import sys
from math import exp
from bitstring import BitArray
from read_SSP import read_SSP
from Browse_ROOT import Browse_ROOT
import os
from smooth_wave import smooth_wave
from baseline_subtract import baseline_subtract
import numpy as np
import glob
from plot_histogram import plot_histogram
from int_input import get_int
import commands
import pickle
import scipy
#  %matplotlib inline


# ##### Book histograms

# In[2]:

def Book_Hist_Time(title, lhist):
    """
    Book histograms, append to a list of histograms
    """

    h_pulse = TH1F(title+'_time, pulses', 'time, pulses', 200, 0., 2000.)
    lhist.append(h_pulse)
    
    h_pulse_high = TH1F(title+'_time, pulses_high', 'time, pulses, high pulse height', 200, 0., 2000.)
    lhist.append(h_pulse_high)
    
    h_wave = TH1F(title+'_time_wf', 'time_wf', 200, 0., 2000.)
    lhist.append(h_wave)
    
        
    h_wave_high = TH1F(title+'_time_wf_high', 'time_wf high ph', 200, 0., 2000.)
    lhist.append(h_wave_high)


    return h_pulse, h_wave, h_pulse_high, h_wave_high


# In[ ]:




# In[3]:

def pl_hist(h):
    """
        draw histogram
    """
    try:
        c
    except NameError:
         c = TCanvas("cv", "cv", 400, 300)
    else:
        pass
       
    h.Draw()
    c.Draw()


# ##### list the existing data files
# 
# broken now.. make a list of voltages/chanels and store the file names for each condition
# wildcard below should identify uniquely the set of files to analyze
# further identifiation: source position/sna, trigger channel,threshold?
# 
# Try to use several file selectors: channel, voltage, source position, trigger
# file selection wild card should make a combination of these selectors unique
# Make a dictionary of datafiles for each combination of the selectors

# In[4]:

def selector(string,key,lkey,lval):
    """
    find a key in a string, insert a value into  a selector set
    """
    print string
    ip = string.find(key)
    print 'key =',key, 'position =',ip
    if ip > -1:
        value = string[ip+lkey:ip+lkey+lval]
        print 'velue = ',value
    else:
        value = 'none'
    
    return value

    
def selector_post(string,key,lkey,lval,sel_set):
    """
    find a key in a string, insert a value into  a selector set
    """
    print string
    ip = string.find(key)
    print 'key =',key, 'position =',ip
    if ip > -1:
        value = string[ip-lval:ip]
        print 'value = ',value
    


# In[5]:

def pulses(waveform,template,tmax,thresh,deltat,tbef,tafter):
    """
    find peaks the waveform
    wave - waveform
    template - template pulse
    tmax - position of the maxium in a template
    threshold - threshold to look for new pulses
    deltat - minimum distance between pulses
    tbef - begining of the serach region
    tafter - end of the search region
    """
    print ' find pulses '
    wave = np.copy(waveform)
    ifig = 0

    tp = []
    ap = []
    plot = False
    lfront = int(np.argmax(template))   # length of template before the  peak 
    #lfront = 100
    lback = int(len(template) - lfront) # length of template after the peak
    
    ibeg = tbef + 0
    iend = tafter + 0
    
    while ibeg < iend:
        
        if plot:
            ifig += 1
            plt.figure(ifig)
            plt.plot(wave)
 
        wh = np.where(wave[ibeg:iend] > thresh)
        if len(wh[0])==0:
            break
        ith = int(wh[0][0] + ibeg)
        #print 'threshold crossing ', ith 
        valmax = np.max(wave[ith:ith+deltat])
        #print wave[ith:ith+deltat]
        posmax =  int(ith + np.argmax(wave[ith:ith+deltat]))
        tp.append(posmax)
        ap.append(valmax)
        #print 'pos ',posmax, ' value ',wave[posmax]
        if plot:
            ifig += 1
            print posmax,lfront,lback,ith,ith+deltat
            plt.figure(ifig)
            plt.plot(wave[posmax-lfront:posmax+lback])
            plt.plot(valmax*template)
            
        for i in range(min(len(template),len(wave)-posmax)):
            wave[posmax-lfront+i] += -valmax*template[i]
        
        ibeg += deltat
    if plot:
        plt.show()
    #print 'done pulses'
    
    return tp,ap


# In[6]:

filedir = 'data/data_Vb_26_5_Vth_5_380nm_50nW_5_Ch9-2016-12-13_19-49-25/'
filenam = 'data_Vb_26_5_Vth_5_380nm_50nW_5_Ch9-2016-12-13_19-49-25.dat'
filedir = 'data/noise_Vb_27_5_Vth_10_Ch9-2016-12-16_16-39-37/'
filedir = 'data/noise_Vb26_0_Vth_10-2016-12-20_15-44-17/'
filedir = '../data/Jan27_2017_data/'
#filedir = '../data/Jan30_2017/'

filedir = '/Users/para/arapuca/data/Tall_Bo/'
filedir = '/Users/para/arapuca/data/Tall_Bo3/'
#filedir = './'
fildat = filedir+filenam
cond = 'F7'
source_pos = '04624'
source_pos = '05132'
filelist = glob.glob(filedir+'*dark*Th_4*dat')
filelist = commands.getoutput('echo "`ls '+filedir+'*dat | grep -v test | grep -v _f1_`"').split('\n')
filelist = commands.getoutput('cd '+filedir+'; echo "`ls *dat | grep -v test | grep -v _f1_`"').split('\n')
filelist = ['Jan27_darks_Vb_22.5_CH_0_1_2_3_5_6_7_8_9_Ch2-2017-01-27_17-20-34.datl']
filelist = ['Jan31_darks_RSat010464_Vb_21_5_Th_6_Ch0125678_F23_Ch2-2017-01-31_10-43-18.dat']
filelist = ["Feb09_darks_Vb_26_5_Vth_12_270_Ch01235678_F5_Ch2-2017-02-09_10-40-58.dat"]
filelist = ['Feb09_RS2000_Vb_25_0_Vth_72_2100_Ch01235678_F17_Ch2-2017-02-09_12-13-52.dat']
filelist = ['Feb09_RS4800_Vb_25_0_Vth_72_2100_Ch01235678_F10_Ch2-2017-02-09_11-50-48.dat']
filelist = ['Feb09_RS5000_TG_CH3_Vb_25_0_Vth_600_Ch01235678_F20_Ch2-2017-02-09_15-11-51.dat']
filelist = commands.getoutput('cd '+filedir+'; echo "`ls *Ch2*.dat`"').split('\n')
voltages = set()
chans = set()
source_pos = set()
trigger = set()
file_coll = {}

#print dir(str)
print 'absasddff'.find('sa')

for file in filelist:
    print file
    #selector(file,'_Vb_',4,4)
    #selector(file,'_Th_',4,1,voltages)
    #selector_post(file,'-2017-',6,1,voltages)
    #selector(file,'_TG_ch',6,1,voltages)
    #ivb = file.find('_Vb_')
    #print ivb,file[ivb+4:ivb+8]
    #ith = file.find('thres')
    #print ith
events = {}
h_ampl = {}
h_ampl_Q = {}


# ##### select data to analyze
# 

# In[ ]:


#print filelist
hist = []
voltage = [1, 2, 3, 4, 5, 6, 7]
chan = ['0','1', '2', '5', '6', '7', '8', '9']
chan = ['0','1', '2', '5', '6', '7', '8' ]
voltage = ['25_5']

voltage = ['21_5', '22.0', '22_5', '23_0', '23_5', '24_0', '24_5', '25_0' ]
#chan = ['0']
print chan


# ##### read requested data files
# 
# to create remplate select pl=True and the average of selected waveforms will be pickled
# otherwise the pickle file is expected to exist

# In[ ]:

# chan = ['3']
# for ch in chan:

    # for volt in voltage:

hist = []
title = ''
h_pulse, h_wave, h_pulse_high, h_wave_high = Book_Hist_Time(title, hist)

    

for file in filelist:

    print 'read file ', file
    events = read_SSP(filedir+file, hex=False, nevmax = 99999)
    nev = len(events)
    print 'number of events' ,nev

    lped = 150                     # window at the beginning to establish baseline
    av_wave = np.zeros(600)
    pl = False
    winlow = 150                    # window to integrate the signal, lower edge
    winhigh = 1000                   # window to integrate the signal, upper edge
    pe = 12.
    
    if pl:
        print 'select the waveforms to create a template'
    else:
        file_template = 'template.ch2'
        t_file = open(file_template, 'rb')
        template =  pickle.load(t_file)
        imax = np.argmax(template)
        t_file.close()
        # plt.plot(template)
        # plt.show()
        # cont = get_int('cont')
    iev = 0
    maxev = 10000                   # maximum number of events to analyze
    print maxev
    
    h_pulse.Reset()
    h_wave.Reset()
    h_pulse_high.Reset()
    h_wave_high.Reset()
    
    nav = 0
    
    for ev in events:
        iev += 1
        print ' event nuber ', iev

        if iev > maxev: 
            continue
        (head, wave) = ev
        base = scipy.mean(wave[0: lped])
        if abs(base-1290)>10:
            continue
        wave3 = baseline_subtract(wave, 0, lped)
        nwfm = smooth_wave(wave3, 20)


        if pl:
            fig = plt.figure(iev)
            plt.title('Event no '+str(iev))
            plt.plot(nwfm)
            #plt.savefig("event_"+str(iev)+"_waveform.png")
            plt.show()
            ii = get_int('select')
            if ii == 1:
                imax = np.argmax(nwfm)
                av_wave += nwfm[imax-100:imax+500]
                nav += 1
            if ii == 2:
                av_wave_n = av_wave/max(av_wave)
                print ' save template'
                file_template = 'template.ch2'
                out = open(file_template, 'wb')
                pickle.dump(av_wave_n, out)
                out.close() 
                plt.plot(av_wave_n)
                plt.show()
        else:
            
            amp_max = max(nwfm[winlow:winhigh])
            charge = sum(nwfm[winlow:winhigh])/(winhigh-winlow)
            thresh = 0.7 * pe
            deltat = 50 
            tbef = 150
            tafter = 1800
            tp,ap = pulses(nwfm,template,imax,thresh,deltat,tbef,tafter)
            
            if amp_max > 3*pe:
                for i in range(1,len(nwfm)):
                    h_wave_high.Fill(i,nwfm[i])
                    for t,p in zip(tp,ap):
                        h_pulse_high.Fill(t,p)
            else:
                
                for t,p in zip(tp,ap):
                    h_pulse.Fill(t,p)
                for i in range(1,len(nwfm)):
                    h_wave.Fill(i,nwfm[i])
            if iev > maxev:
                raise KeyboardInterrupt     # stop after one event
#
    
    print 'done'
    hist_file = 'hist/'+file+'_time.hist'
    fr = TFile(hist_file, 'recreate')
    for h in hist:
        h.Write()
    fr.Close()



# ##### analyze data
# 
# use window [0,lped] to determine and subtract the current baseline
# <nl>
# <li> aa
# </nl>

# In[ ]:

#####  

for ch in chan:
    for volt in voltage:
        lped = 150                     # window at the beginning to establish baseline
        av_wave = np.zeros(2000)
        pl = False
        winlow = 150                    # window to integrate the signal, lower edge
        winhigh = 1000                   # window to integrate the signal, upper edge

        iev = 0
        maxev = 10000                   # maximum number of events to analyze
        print maxev

        h_ampl[ch,volt].Reset()
        h_ampl_Q[ch,volt].Reset()

        for ev in events[ch,volt]:
            iev += 1
            if iev > maxev: 
                continue
            (head, wave) = ev
            wave3 = baseline_subtract(wave, 0, lped)
            nwfm = smooth_wave(wave3, 20)

            amp_max = max(nwfm[winlow:winhigh])
            #print amp_max
            charge = sum(nwfm[winlow:winhigh])/(winhigh-winlow)
            h_ampl[ch,volt].Fill(amp_max)
            h_ampl_Q[ch,volt].Fill(amp_max, charge)

            if pl:
                fig = plt.figure()
                plt.plot(nwfm)
                plt.show()
                # ii = get_int('input')
            av_wave += nwfm/nev

print 'done'

#Browse_ROOT()


# pl_hist(h_ampl[ch,volt])
# pl_hist(h_ampl_Q[ch,volt])
# 
# #plot_histogram(h_ampl)
# #plot_histogram(h_ampl_Q)
# 
# #plt.plot(av_wave)
# #plt.title(title)
# #plt.show()
# #exit()

# hist_file = 'source_data_'+cond+'.hist'
# fr = TFile(hist_file, 'recreate')
# for h in hist:
#     h.Write()
# fr.Close()

# ##### get output of shell command

# import commands
# aa = commands.getstatusoutput("ls ..")[1].split()
# print type(aa)
# print aa
# aa = commands.getstatusoutput("pwd")
# print type(aa)
# print aa

# In[ ]:

## ii = get_int('type')
#print ii
#print hist

arr = np.zeros(200)
arrb = np.zeros(500)
res = arr-arrb
print len(res)

thresh = 50
wh = np.where(arr > thresh)
print wh, len(wh), len(wh[0])


# In[ ]:



