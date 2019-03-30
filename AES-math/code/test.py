import sys, os
import aes_info_plus

from file_io import load_data, load_int_data
from gmath import gmultiply as gm
from gdict import logD, antilogD

# --------------------------------------------

exp  = load_int_data('g3.powers.int.txt')
logs = load_int_data('g3.logs.int.txt')
mi   = load_data('mi.txt')

# --------------------------------------------

def test_mi():
    print("test mult inverses v. gmultiply")
    for t in mi: 
        a,b = t.split(',')
        x,y = int(a),int(b)
        assert gm(x,y) == 1
        assert gm(y,x) == 1

# 'g3.powers.int.txt'
# dicts made directly from that
# test if logs correctly written to file

def test_logs():
    print("test log dict")
    # missing entry for 0 because log 0 undefined
    for i,v in enumerate(logs):
        # increment i b/c first entry is log(1)
        assert v == logD[i+1]

# compare log mult to gmultiply
def test_log_mult():
    print("test log multiply v. gmultiply")
    print("also test gmultiply order")
    for i in range(1,256):
        for j in range(1,256):
            # value from gmutiply
            p1 = gm(i,j)  
            p2 = gm(j,i)
            assert p1 == p2
             
            # value from logs
            r = logD[i] + logD[j]
            if r >= 255:
                r -= 255
            p3 = antilogD[r] 
            assert p1 == p3

def get_table(s):
    D = {'x2':aes_info_plus.x2,
         'x3':aes_info_plus.x3,
         'x9':aes_info_plus.x9,
         'x11':aes_info_plus.x11,
         'x13':aes_info_plus.x13,
         'x14':aes_info_plus.x14 }
    return D[s]
        
def load_table(s):
    s = get_table(s)
    table = list()
    for line in s.strip().split('\n'):
        line = line.replace(',',' ')
        line = line.strip().split()
        sL = [int(h,base=16) for h in line]
        table.extend(sL)
    return table

# from wikipedia originally?       
def test_times_tables():
    print("test times tables")
    for n in [2,3,9,11,13,14]:
        L = load_table('x' + str(n))
        for i,v in enumerate(L):
            assert gm(n,i) == v


for f in [test_mi, 
          test_logs, 
          test_log_mult,
          test_times_tables]:
    f()
