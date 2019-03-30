import sys

if len(sys.argv) < 4:
    print "provide args:  hex|int x y"
    sys.exit()

from aes_std_math import *
from aes_exp_math import *

mode, m, n = sys.argv[1:]

if mode == 'int':
    x = int(m)
    y = int(n)

else:
    x = int(m,16)
    y = int(n,16)

p = timesX(x,y)
print 'x', x, 'y', y, 'p', p, hex(p)[2:].zfill(2)


