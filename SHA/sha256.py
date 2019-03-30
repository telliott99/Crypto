import sys
from funcs import *
import bits
from pad_sha256 import *

bits.w = 32

# ===============================================

fn = sys.argv[1]
fh = open(fn)
data = fh.read()
fh.close()
iL = [ord(c) for c in data]

mL = pad_data(iL)
for i,word in enumerate(mL):
    pbin(word,'mL' + str(i))

# ===============================================

# SHA-256 has additional functions 
# not seen in SHA-1
S0 = S0_256   # from utils.py
S1 = S1_256
s0 = s0_256
s1 = s1_256

# ===============================================

rL = getRegisterConstants()
rL = [int(e[:8],16) for e in rL]

# components of initial hash value
H0 = rL[0]    # 'int(6a09e667)'
H1 = rL[1]
H2 = rL[2]
H3 = rL[3]
H4 = rL[4]
H5 = rL[5]
H6 = rL[6]
H7 = rL[7]

hnames = ['H0','H1','H2','H3',
          'H4','H5','H6','H7']
hL = [H0,H1,H2,H3,H4,H5,H6,H7]

for value,char in zip(hL,hnames):
    pbin (value,char)

# kL from funcs.py
kL = getKConstants()
kL = [int(hv[:8],16) for hv in kL]

print '-' * 20

# ===============================================

block = 1

while mL:
    print 'block', block
    block += 1
    wL = mL[:16]
    mL = mL[16:]

    # need to expand wL to consist of 64 entries
    def expand(wL):
        for i in range(16,64):
            tmp = ADD(s1(wL[i-2]),
                      wL[i-7],
                      s0(wL[i-15]),
                      wL[i-16])
                      
            wL.append(tmp)
        return wL
    
    wL = expand(wL)
    
    for i,word in enumerate(wL):
        pbin(word,'wL' + str(i))
    
    print '-' * 20

    a = H0
    b = H1
    c = H2
    d = H3
    e = H4
    f = H5
    g = H6
    h = H7
    
    zL = zip([a,b,c,d,e,f,g,h],'abcdefgh')
    for value,char in zL:
        pbin(value,char)
    print
            
# ===============================================
        
    # 64 rounds for each block:
    
    for t in range(64):
        print 'round =', t
        
        W = wL[t]
        pbin(W, 'W')
        
        K = kL[t]
        pbin(K, 'K')
    
        # same function each round
        tmp1 = S1(e)
        tmp2 = Ch(e,f,g)
        T1 = ADD(h,tmp1,tmp2,K,W)
        T2 = ADD(S0(a),Maj(a,b,c))
    
        h = g
        g = f
        f = e
        e = ADD(d,T1)
        d = c
        c = b
        b = a
        a = ADD(T1,T2)
        
        print 'after assignment a-h'
        zL = zip('abcdefgh', (a,b,c,d,e,f,g,h))
        for char,value in zL:
            pbin(value,char)
               
        print '-' * 20
    
    print 'update H0-H7'
    H0 = ADD(a,H0)
    H1 = ADD(b,H1)
    H2 = ADD(c,H2)
    H3 = ADD(d,H3)
    H4 = ADD(e,H4)
    H5 = ADD(f,H5)
    H6 = ADD(g,H6)
    H7 = ADD(h,H7)
    
    print 'after final ADD'
    hL = [H0,H1,H2,H3,H4,H5,H6,H7]
    
    for value,char in zip(hL,hnames):
        pbin (value,char)

print 'block #', block
print 'final hash:'
print ' '.join(hex(v)[2:].zfill(8) for v in hL)

    
