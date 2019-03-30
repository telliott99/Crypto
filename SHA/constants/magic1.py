# python magic1.py > magic1.txt

from decimal import *
from math import sqrt

def doOne(n,N):
    n = Decimal(n).sqrt()
    pL = list()
    for i in range(N):
        m = (n*16) % 16
        v = int(m)
        n = m - v
        h = hex(v)
        pL.append(h[2])
    return ''.join(pL)

for p in [2,3,5,7,11,13,17,19]:
    print str(p).rjust(2), doOne(p,16)
