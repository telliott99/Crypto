import aes_utils as ut
import aes_info

SZ = 16
SBox = aes_info.AES_Sbox_encrypt

def print_schedule(sched):
    pL = ut.chunks(sched, n=4)
    for i,kL in enumerate(pL):
        print str(i).rjust(2), "       ",
        printHex(kL)
    print

def print_schedule_as_hex(L):
    for i,k in enumerate(L):
        if i and i % 4 == 0:  print
        hL = [hex(n)[2:].zfill(2) for n in k]
        print str(i).rjust(2),
        print ' '.join(hL),
        print k

def printHex(L):
    for i in range(0,len(L),4):
        pL = list()
        for chunk in L[i:i+4]:
            pL.extend(chunk)
        hL = [hex(n)[2:].zfill(2) for n in pL]
        print ' '.join(hL)

def getKeySchedule(input, mode='str'):
    if mode == 'str':
        s = padKey(input)
        kL = processTextKey(s)
    elif mode == 'hex':
        hL = input.strip().split()
        kL = [int(h,16) for h in hL]
    else:
        kL = input
    assert len(kL) == SZ
    kL = ut.chunks(kL,4)
    return expand_key(10, kL)

#------------------------------

# takes key as str
def padKey(key, padChar = None):
    n = SZ - (len(key) % SZ)
    if n % 16 == 0:
        return key
    if padChar:
        return key + padChar * n
    p = n
    pad = ''.join([chr(p) for p in [p]*p])
    return key + pad

# takes padded key as str
def processTextKey(key):
    return [ord(c) for c in key]

# rotates word left by one *entire* byte
def rotate_left(w):
    return w[1:] + w[:1]
    
# RC: round constant
def RC_generator():
    # we xor etc when > 128
    bL = [1, 2, 4, 8, 16, 32, 64, 
          128, 27, 54, 108, 216, 
          171, 77, 154, 47]
    for b in bL:
        yield [b] + [0,0,0]

def g(w, RC):
    global SBox
    u = rotate_left(w)
    # 0-based index
    v = [SBox[n] for n in u]
    return ut.xorTwoWords(RC,v)

def oneRound(RC, key_schedule):
    L = key_schedule[:]
    # u0,u1,u2,u3 are the last four words
    u0,u1,u2,u3 = L[-4:]
    u4 = ut.xorTwoWords(g(u3,RC),u0)
    
    L.append(u4)
    L.append(ut.xorTwoWords(L[-1],u1))
    L.append(ut.xorTwoWords(L[-1],u2))
    L.append(ut.xorTwoWords(L[-1],u3))
    return L
    
# input is a list of 16 ints in groups of four
def expand_key(n, key_schedule):
    L = key_schedule[:]
    gen = RC_generator()
    for i in range(n):
        RC = gen.next()
        L = oneRound(RC, L)
    return L
