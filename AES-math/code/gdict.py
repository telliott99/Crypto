import os
from file_io import load_int_data

expL = load_int_data('g3.powers.int.txt')

logD = dict()
antilogD = dict()

for i,v in enumerate(expL):
    # do not overwrite for 255,01
    if i == 255:
        continue
    # (0,1), (1,3), (2,5) ..
    logD[v] = i
    antilogD[i] = v

