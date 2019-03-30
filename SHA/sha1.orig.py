# python sha1.orig.py > abc_sha1.txt

from funcs import *
import bits
bits.v = False
bits.w = 32

# the padded message block
# SHA-1 uses 512 bits as 16 @ 32-bit words

input = '''
61626380
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
00000018
'''

# number of octal '0's above is
# 1 + (8 * 14) + 6 = 119, that's 4 x 119 =
#  476 bits
# +  4 from the '8' 
# +  1 from the '1'
# plus the other bits including
# + 25 from '6162638'
# = 512


iL = input.strip().split('\n')
wL = [int(s,16) for s in iL]
    
# need to expand wL to consist of 80 entries
def expand(wL):
    for i in range(16,80):
        tmp = XOR(wL[i-3],wL[i-8],
                  wL[i-14],wL[i-16])
        wL.append(ROTL(tmp,1))
    return wL

wL = expand(wL)

for i,word in enumerate(wL):
    if i == 16:
        print '-' * 20
    pbin(word,'wL' + str(i))

print '-' * 20

# components of initial hash value (from funcs)
# these are *not* magic1 or magic2 constants

H0 = int(H0,16)    # 'int(0x67452301)'
H1 = int(H1,16)
H2 = int(H2,16)
H3 = int(H3,16)
H4 = int(H4,16)

hnames = ['H0','H1','H2','H3','H4']
hL = [H0,H1,H2,H3,H4]

for value,char in zip(hL,hnames):
    pbin (value,char)

print '-' * 20
    
# ===============================================

def fK(t):
    # SHA-1 functions and constants fips 9-10
    if 0 <= t <= 19:
        f = Ch
        K = int(K0,16)
    elif 20 <= t <= 39:
        f = Parity
        K = int(K20,16)
    elif 40 <= t <= 59:
        f = Maj
        K = int(K40,16)
    elif 60 <= t <= 79:
        f = Parity 
        K = int(K60,16)
    return f,K

# ===============================================

a = H0
b = H1
c = H2
d = H3
e = H4

for value,char in zip([a,b,c,d,e],'abcde'):
    pbin(value,char)
print

# ===============================================

# 80 rounds:

for t in range(80):
    print 'round =', t
    
    W = wL[t]
    pbin(W, 'W')
    
    f,K = fK(t)
    pbin(K, 'K')

    tmp1 = ROTL(a,5)
    pbin(tmp1,'tmp1')
    tmp2 = f(b,c,d,names='bcd')
    pbin(tmp2,'tmp2')
    
    print '-' * 10

    T = ADD(tmp1,tmp2,e,K,W)
    e = d
    d = c
    c = ROTL(b,30)
    b = a
    a = T
    
    print 'after assignment a-e'
    for char,value in zip('abcde', (a,b,c,d,e)):
        pbin(value,char)
           
    print '-' * 20

print 'update H0-H4'
H0 = ADD(a,H0)
H1 = ADD(b,H1)
H2 = ADD(c,H2)
H3 = ADD(d,H3)
H4 = ADD(e,H4)

print 'after final ADD'
hL = [H0,H1,H2,H3,H4]

for value,char in zip(hL,hnames):
    pbin (value,char)

print ' '.join(hex(v)[2:].zfill(8) for v in hL)

    
    