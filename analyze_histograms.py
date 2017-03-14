
# coding: utf-8

# ##### import files

# In[ ]:

import commands
from histograms_from_file import ldir
from ROOT import TFile, gDirectory, TH1F
from plot_histogram import plot_histogram
from overlay_histograms import overlay_histograms


# ##### list the existing data files

# In[ ]:

def selector(string,key,lkey,lval, sel_set):
    """
    find a key in a string, insert a value into  a selector set
    """
    print string
    ip = string.find(key)
    print 'key =',key, 'position =',ip
    if ip > -1:
        value = string[ip+lkey:ip+lkey+lval]
        print 'value = ',value
        sel_set.add(value)
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
        
def selector_field(string,key,sep):
    """
    find a key in a string, insert a value into  a selector set
    """
    print string
    tok = string.split(sep)
    for i in range(len(tok)):
        if tok[i] == key:
            value = tok[i+1]
    
    return value


# In[ ]:

print 'aa'
filedir = '/Users/para/arapuca/arapuca_analysis/hist'
#files = commands.getoutput('echo "`ls  '+filedir+'`"*RS550*Vb_25_0*Ch2*hist').split('\n')
files = commands.getoutput('cd '+filedir+'; echo "`ls *RS50*Vb_25_0*Ch2*dat.hist`"').split('\n')
print 'bb'
mfiles = []
for f in files:
    g = f.replace('selfTG','TG_CH2')
    mfiles.append(g)
    print f
    
fil = []
csv_fil = []
dat_fil = []
lenfil = []


voltages = set()
chans = set()
source_pos = set()
trigger = set()
file_coll = {}

tr = []
thr = []
for f in mfiles:
    print f
    #selector(f,'_Vb_',4,4,voltages)
    #selector(file,'_Th_',4,1,voltages)
    #selector_post(file,'-2017-',6,1,voltages)
    tr.append(selector(f,'_TG_CH',6,1,trigger))
    thr.append(selector_field(f,'Vth','_'))
    #ivb = file.find('_Vb_')
    #print ivb,file[ivb+4:ivb+8]
    #ith = file.find('thres')
    #print ith
    

for f,trig,thresh in zip (mfiles,tr,thr):
    print f,trig,thresh

datf = [
    'Feb09_RS5000_TG_CH3_Vb_25_0_Vth_290_Ch01235678_F1_Ch2-2017-02-09_12-32-41.dat.hist',
    'Feb09_RS5000_TG_CH3_Vb_25_0_Vth_600_Ch01235678_F20_Ch2-2017-02-09_15-11-51.dat.hist',
    'Feb09_RS5000_TG_CH2_Vb_25_0_Vth_14_Ch01235678_F11_Ch2-2017-02-09_13-09-42.dat.hist',
    'Feb10_RS5000_selfTG_Vb_25_0_Vth_40_500_Ch01235678_F1_Ch2-2017-02-10_07-45-48.dat.hist',
    'Feb10_RS5000_selfTG_Vb_25_0_Vth_50_600_Ch01235678_F1_Ch2-2017-02-10_07-52-24.dat.hist',
    'Feb10_RS5000_selfTG_Vb_25_0_Vth_60_700_Ch01235678_F1_Ch2-2017-02-10_07-56-30.dat.hist',
    'Feb09_RS5000_TG_CH2_Vb_25_0_Vth_72_Ch01235678_F21_Ch2-2017-02-09_15-15-37.dat.hist',
    'Feb09_RS5000_TG_CH2_Vb_25_0_Vth_72_Ch01235678_F24long_Ch2-2017-02-09_15-36-41.dat.hist',
    'Feb10_RS5000_selfTG_Vb_25_0_Vth_104_1100_Ch01235678_F5_Ch2-2017-02-10_08-01-02.dat.hist',
    'Feb10_RS5000_selfTG_Vb_25_0_Vth_200_2200_Ch01235678_F6_Ch2-2017-02-10_08-06-17.dat.hist',
    ]

histograms = []
for f in datf:
    hh = []
    MyFile = TFile(filedir+'/'+f)  
    gDirectory.pwd()
    dir = gDirectory
    lhist = ldir(dir,MyFile)
    print lhist
    for h in lhist:
        hst = h.ReadObj().Clone()
        hh.append(hst)
        hst.SetDirectory(0)
    histograms.append(hh)

    print f

l_lim = [0, 0, 12, 37, 50, 60,70, 74,95,220]
u_lim = []
for  i in range(len(l_lim)-1): 
    u_lim.append(l_lim[i+1])
u_lim.append(300)

print l_lim
print u_lim

for l,u in zip(l_lim,u_lim):
    print l,u

cont_l = []
cont_h = []

for hist, fil, l,h in zip(histograms,datf,l_lim,u_lim):
    print fil
    hh = hist[1]
    print hh.GetEntries()
    nb = hh.GetNbinsX()
    print nb
    cl = hh.Integral(l,nb)
    ch = hh.Integral(h,nb)
    ov = hh.GetBinContent(nb+1)
    print ov
    cont_l.append(cl+ov)
    cont_h.append(ch+ov)
    #exit()
    #plot_histogram(hist[1])
    

print cont_l
print cont_h

nf = [1.]
for i in range(1,len(cont_l)):
    nf.append(nf[i-1]*cont_h[i-1]/cont_l[i])

print nf

h_ov = []
for h,f in zip(histograms,nf):
    h[3].Rebin(5)
    h[3].Scale(f)
    h_ov.append(h[3])
    #plot_histogram(h[3])
    
print h_ov 
overlay_histograms(h_ov,option = ' e ',op='add')


# In[ ]:

print dir(commands)


# ##### analyze data
# 
# use window [0,lped] to determine and subtract the current baseline
# <nl>
# <li> aa
# </nl>

# ##### get output of shell command

# In[ ]:

import commands
aa = commands.getstatusoutput("ls ..")[1].split()
print type(aa)
print aa
aa = commands.getstatusoutput("pwd")
print type(aa)
print aa

