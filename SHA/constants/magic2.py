# python magic2.py > magic2.txt
'''
output:
  2 428a2f98d728ae22
..
409 6c44198c4a475817

matches p 10 of 
http://csrc.nist.gov/publications/fips/fips180-2/fips180-2.pdf
'''

from decimal import *

def cube_root(x):
    return Decimal(x) ** (Decimal(1) / Decimal(3))

def doOne(n,N):
    n = cube_root(n)
    pL = list()
    for i in range(N):
        m = (n*16) % 16
        v = int(m)
        n = m - v
        h = hex(v)
        pL.append(h[2])
    return ''.join(pL)

fn = 'primes80.txt'
fh = open(fn,'r')
data = fh.read().strip().split()
primes = [int(e) for e in data]
fh.close()

for p in primes:
    print str(p).rjust(3), doOne(p,16)
