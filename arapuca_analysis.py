
# coding: utf-8

# ##### import files

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

#  %matplotlib inline


# ##### Book histograms

# In[2]:

def Book_Hist(title, lhist):
    """
    Book histograms, append to a list of histograms
    """

    h_ampl = TH1F(title+'_amx_amplitude', 'max amplitude', 50, 0, 0)
    lhist.append(h_ampl)
    h_ampl_Q = TH2F(title+'_amx_amplitude_Q', 'Charge vs max amplitude',
                    100, 0, 100, 100, 0., 100.)
    lhist.append(h_ampl_Q)
    return h_ampl, h_ampl_Q


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

# In[4]:

filedir = 'data/data_Vb_26_5_Vth_5_380nm_50nW_5_Ch9-2016-12-13_19-49-25/'
filenam = 'data_Vb_26_5_Vth_5_380nm_50nW_5_Ch9-2016-12-13_19-49-25.dat'
filedir = 'data/noise_Vb_27_5_Vth_10_Ch9-2016-12-16_16-39-37/'
filedir = 'data/noise_Vb26_0_Vth_10-2016-12-20_15-44-17/'
filedir = '../data/Jan25_2017_data/'
fildat = filedir+filenam

filelist = glob.glob(filedir+'*.dat')
for file in filelist:
    print file
    
  


# ##### select data to analyze
# 

# In[5]:


#print filelist
hist = []
voltage = [1, 2, 3, 4, 5, 6, 7]
chan = ['0','1', '2', '5', '6', '7', '8']
voltage = ['21_7']
chan = ['5']
print chan


# ##### read requested data files

# In[6]:

events = {}
h_ampl = {}
h_ampl_Q = {}

for ch in chan:

    for volt in voltage:
        
        file = filedir+'data_Vb_'+str(volt)+'*Ch'+ch+'*dat'
        title = 'Ch '+ch + ' V bias = '+str(volt)+ 'V'
        h_ampl[ch,volt], h_ampl_Q[ch,volt] = Book_Hist(title, hist)
        
        dfile = glob.glob(file)
        if len(dfile) != 1:
            print ' non unique data file', file
        
        print 'read file ', dfile
        events[ch,volt] = read_SSP(dfile[0])

        nev = len(events[ch,volt])
        print 'number of events' ,nev



# ##### analyze data
# 
# use window [0,lped] to determine and subtract the current baseline
# <nl>
# <li> aa
# </nl>

# In[ ]:

#####  

lped = 150                     # window at the beginning to establish baseline
av_wave = np.zeros(2000)
pl = True
winlow = 150                    # window to integrate the signal, lower edge
winhigh = 300                   # window to integrate the signal, upper edge

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
    if pl:
        fig = plt.figure()
        plt.plot(nwfm)
        plt.show()
        # ii = get_int('input')
    av_wave += nwfm/nev
    amp_max = max(nwfm[winlow:winhigh])
    charge = sum(nwfm[winlow:winhigh])/(winhigh-winlow)
    h_ampl[ch,volt].Fill(amp_max)
    h_ampl_Q[ch,volt].Fill(amp_max, charge)
print 'done'

#Browse_ROOT()

pl_hist(h_ampl[ch,volt])
pl_hist(h_ampl_Q[ch,volt])

#plot_histogram(h_ampl)
#plot_histogram(h_ampl_Q)

#plt.plot(av_wave)
#plt.title(title)
#plt.show()
#exit()


# In[ ]:

print h_ampl
pl_hist(h_ampl_Q)


# ##### get output of shell command

# In[ ]:

import commands
aa = commands.getstatusoutput("ls")[1].split()
print type(aa)
print aa


# In[ ]:

ii = get_int('type')
print ii

