#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 13:44:07 2017

@author: para
"""

import matplotlib.pyplot as plt

t3_rates = {
            '6100': 6800,
            '6600': 6600,
            '7400': 700,
            '5500': 6260,
            '4800': 1000,
            '4500': 150,
            '3900': 65,
            '2600': 65
            }
    
pos = []
rate = []
for key in t3_rates:
    pos.append(int(key))
    rate.append(t3_rates[key])
    
for p,r in zip(pos,rate):
    plt.plot(p,r,'*')
  
    plt.title('T3 trigger rates as a function of position')
plt.show()