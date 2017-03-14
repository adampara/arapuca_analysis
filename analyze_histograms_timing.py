
# coding: utf-8

# ##### import files

# In[1]:

import commands
from histograms_from_file import ldir
from ROOT import TFile, gDirectory, TH1F
from plot_histogram import plot_histogram
from overlay_histograms import overlay_histograms


# ##### list the existing data files

# In[2]:

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
files = commands.getoutput('cd '+filedir+'; echo "`ls Feb*TG_CH2*Ch2*time.hist | grep -v TG_CH3`"').split('\n')
print 'bb'
mfiles = []
for f in files:
    g = f.replace('selfTG','TG_CH2')
    mfiles.append(g)
    print f
    


histograms = []
for f in files:
    print f
    hh = []
    MyFile = TFile(filedir+'/'+f)  
    gDirectory.pwd()
    dir = gDirectory
    lhist = ldir(dir,MyFile)
    #print lhist
    for h in lhist:
        hst = h.ReadObj().Clone()
        # plot_histogram(hst)
        hh.append(hst)
        hst.SetDirectory(0)
    histograms.append(hh)

h_summed = []
for ht in range(4):
    h_ov = []
    for hh in histograms:
        h_ov.append(hh[ht])
        
    h_summed.append(overlay_histograms(h_ov,option = ' e ',op='add'))

hist_file = 'hist/summed_time_TG_CH2*Ch2.hist'
fr = TFile(hist_file, 'recreate')
for h in h_summed:
    h.Write()
fr.Close()


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

