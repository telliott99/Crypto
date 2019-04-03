import utils as ut
import aes_info

SZ = 16

s = aes_info.AES_Sbox_encrypt
SBox = [int(c) for c in s.strip().split()]

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

def xor_word(r,v):
    ret = [x ^ y for x,y in zip(r,v)]
    return ret

# rotates word left by one *entire* byte
def rotate_left(w):
    return w[1:] + w[:1]

def g(w, RC):
    global SBox
    u = rotate_left(w)
    # 0-based index
    v = [SBox[n] for n in u]
    return xor_word(RC,v)

def oneRound(RC, key_schedule):
    L = key_schedule[:]
    # u0,u1,u2,u3 are the last four words
    u0,u1,u2,u3 = L[-4:]
    u4 = xor_word(g(u3,RC),u0)
    
    L.append(u4)
    L.append(xor_word(L[-1],u1))
    L.append(xor_word(L[-1],u2))
    L.append(xor_word(L[-1],u3))
    return L
    
# RC: round constant
def RC_generator():
    # do we xor etc when > 127 or > 128 ?
    bL = [1, 2, 4, 8, 16, 32, 64, 
          128, 27, 54, 108, 216, 
          171, 77, 154, 47]
    for b in bL:
        yield [b] + [0,0,0]

# input is a list of 16 ints in groups of four
def expand_key(n, key_schedule):
    L = key_schedule[:]
    gen = RC_generator()
    for i in range(n):
        RC = gen.next()
        L = oneRound(RC, L)
    return L

#------------------------------

def print_schedule(L):
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

def ex1():
    key = 'hello'
    key = padKey(key, padChar = '0')
    kL = processTextKey(key)
    return ut.chunks(kL,4)

def ex2():
    return ut.chunks(range(16),4)
    
def ex3():
    key_schedule = [[15,21,113,201],
                    [71,217,232,89],
                    [12,183,173,214],
                    [175,127,103,152]]
    return key_schedule

def ex4():
    key = 'Thats my Kung Fu'
    kL = [ord(c) for c in key]
    return ut.chunks(kL,4)

def ex5():
    key_schedule = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]
    return key_schedule

def ex6():
    input = [
        '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00',
        'ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff',
        '00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f',
        '69 20 e2 99 a5 20 2a 6d 65 6e 63 68 69 74 6f 2a']
        
    for s in input:
        k = [int(h,16) for h in s.strip().split()]
        kL = ut.chunks(k,4)
        L = expand_key(10, kL)
        printHex(L[:4] + L[-4:])
        print

def do_example(ex):
    key_schedule = ex()       
    L = expand_key(10, key_schedule)
    print_schedule(L)
    
if __name__ == "__main__":
    #do_example(ex5)
    ex6()

   



