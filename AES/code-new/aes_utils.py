import random

SZ = 16 

# we allow key and plaintext to be:
# list of ints
# hex string
# plaintext string 

def convert(s):
    if type(s) == type([1,2,3]):
        v = s[0]
        if type(v) == type(2):
            return s
        if type(v) == type('abc'):
            return [int(c,base=16) for c in s]
    if type(s) == type('abc'):
        L = s.strip().split()
        try:
            hL = [hex(h) for h in L]
            return [int(h,base=16) for h in hL]
        except:
            return [ord(c) for c in s]

def printable(L):
    return ' '.join([hex(n)[2:].zfill(2) for n in L])

def pad(p):
    p = p[:SZ]
    if len(p) < SZ:
        x = SZ - len(p)
        p += "X" * x
    return p

def pad_key(k):
    s = 'abcdefghijklmnopqrstuvwxyz'
    s += '0123456789'

    if len(k) < SZ: 
        print("Key was too short so I added some more.")
        while len(k) < SZ:
            k += random.choice(s)
    return k


