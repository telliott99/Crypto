import numpy as np

def show(L, s=None):
    if s:
        print(s)
    a = np.array(L)
    a.shape = (4,4)
    pL = list()
    for e in a.transpose():
        iline = [str(n).rjust(3) for n in e]
        hline = [hex(int(n))[2:].zfill(2) for n in e]
        pL.append(' '.join(iline) + ' | ' + ' '.join(hline))
    print('\n'.join(pL))

def input(s):
    sL = s.strip().split()
    return [int(c) for c in sL]
    
