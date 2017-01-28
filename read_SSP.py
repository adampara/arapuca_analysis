# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 14:30:43 2017

@author: para
"""
import matplotlib.pyplot as plt
from bitstring import BitArray
import numpy as np

def read_SSP(file, hex=True):
    """
    Read the data file with SSP information
    """
    f = open(file)

    if hex:
        lines = [int(x,16) for x in f.read().splitlines()]
    else:
        lines = [int(x) for x in f.read().splitlines()]   

    
    nhead = 24      # length of header (in16 bit words)
    nsh = 2**16     # factor to shift by 16 bits

    pointer = 0     # pointer to the beginning of a current waveform
    loop = True
    events = []      # assemble data in to events (header,waveform)

    while loop:

        head = []   # assemble the header, Manual Version 2.06
        for kk in range(nhead):
            k = kk - pointer
            if k % 2 == 1:    # assemble 16 bits words into 32,
                head.append(lines[k-1] + nsh*lines[k])

        rl = BitArray(uint=head[1], length=32)[16:32].uint   # record length
        ch = BitArray(uint=head[2], length=32)[12:16].uint   # chanel number

        peak_off = BitArray(uint=head[5], length=32)[0:8].uint
        peak_sum = BitArray(uint=head[5], length=32)[8:32].uint

        bas_sum = BitArray(uint=head[6], length=32)[8:32].uint
        integrated_sum_7_0 = BitArray(uint=head[6], length=32)[0:8].uint

        integrated_sum_23_8 = BitArray(uint=head[7], length=32)[16:32].uint
        baseline_offset = BitArray(uint=head[7], length=32)[0:16].uint

        cfd0 = BitArray(uint=head[8], length=32)[16:32].uint
        cfd1 = BitArray(uint=head[8], length=32)[0:16].uint
        cfd2 = BitArray(uint=head[9], length=32)[16:32].uint
        cfd3 = BitArray(uint=head[9], length=32)[0:16].uint

        local_ev_timestamp_15_0 = BitArray(uint=head[10], length=32)[0:16].uint
        fractional_timestamp = BitArray(uint=head[10], length=32)[16:32].uint
        local_ev_timestamp_47_16 = head[11]

        ev_header = (ch, peak_off, peak_sum, integrated_sum_7_0, bas_sum,
                     baseline_offset, integrated_sum_23_8,
                     cfd0, cfd1, cfd2, cfd3,
                     local_ev_timestamp_15_0, fractional_timestamp,
                     local_ev_timestamp_47_16)

        wave = []
        for i in range(nhead, 2*rl):
            wave.append(BitArray(uint=int(lines[pointer+i]),
                                 length=16)[2:16].uint)

        events.append((ev_header, np.array(wave)))

        pointer += 2*rl

        if pointer == len(lines):
            loop = False

    return events
