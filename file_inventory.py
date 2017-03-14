
# coding: utf-8

# ##### import files

# In[1]:

import commands


# ##### list the existing data files

# In[43]:


filedir = '/Users/para/arapuca/data/Tall_Bo'
files = commands.getoutput('echo "`ls  -l '+filedir+'`"').split('\n')


fil = []
csv_fil = []
dat_fil = []
lenfil = []
for f in files[1:]:
    tok = f.split()
    fil.append(tok[8])
    lenfil.append(tok[4])
    if f[-4:] == '.csv':
        csv_fil.append(tok[8])
    if f[-4:] == '.dat':
        dat_fil.append(tok[8])

for f in csv_fil:
    print f

for f,l in zip(fil,lenfil):
    print '{:>12}, {:<80}'.format(l,f)


# In[20]:

print dir(commands)


# ##### analyze data
# 
# use window [0,lped] to determine and subtract the current baseline
# <nl>
# <li> aa
# </nl>

# ##### get output of shell command

# In[9]:

import commands
aa = commands.getstatusoutput("ls ..")[1].split()
print type(aa)
print aa
aa = commands.getstatusoutput("pwd")
print type(aa)
print aa

