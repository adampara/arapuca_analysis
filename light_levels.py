#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 20:54:50 2017

@author: para
"""
import collections
import math
pos = {'f7': 5132, 'f8':5132, 'f10':4624}

f7 = {'0':1972, '1':1487, '2':722, '5':1824, '6':1909, '7':1782, '8':1005}
f8 = {'0':1972, '1':1547, '2':743, '5':1796, '6':1930, '7':1800, '8':1016}
f10 = {'0':1880, '1':1755, '2':747, '5':1168, '6':1800, '7':1832, '8':758}

chan = ['0', '1', '2', '3', '5', '6', '7', '8']
nzero = {}

for  key in f7:
    nzero[key,'f7'] = f7[key]
    
for  key in f8:
    nzero[key,'f8'] = f8[key]

for  key in f10:
    nzero[key,'f10'] = f10[key]
    
for key in nzero:
    print key[0], key[1], pos[key[1]], nzero[key]
        
od = collections.OrderedDict(sorted(nzero.items()))
print od
print '-----------------------------------------------------------------'

print '{:>12}  {:>12}  {:>12} {:>20}'.format('channel no','position','n(0)','      no of photons')
oc = -1
nev = 2001
for key in od:
    #print key, od[key]
    if key[0] != oc:
        oc = key[0]
        print '-----------------------------------------------------------------'

    nz = od[key]
    print '{:>12}  {:>12}  {:>12}  {:12.03f} {:>2} {:5.03f} '.format(key[0], pos[key[1]], 
      od[key],-math.log(float(od[key])/nev),'+-',
      math.sqrt(nz*(nev-nz)/nev)/nz)

print '-----------------------------------------------------------------'