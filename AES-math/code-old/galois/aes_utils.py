def readData(fn, mode = 'r'):
    FH = open(fn, mode)
    data = FH.read()
    FH.close()
    return data

def writeData(fn, data, mode = 'w'):
    FH = open(fn, mode)
    FH.write(data)
    FH.close()

def chunks(iterable, n):
    rL = list()
    while iterable:
        rL.append(iterable[:n])
        iterable = iterable[n:]
    return rL

# construct string for printing
# space every SZ, newline every

def pchunks(L, SZ=7, ONELINE=4):
    pL = list()
    cL = chunks(L, SZ)
    for i, sL in enumerate(cL):
        if i:
            if i % ONELINE == 0:
                pL.append('\n')
            else:
                pL.append(' ')
        pL.append(''.join(sL))
    return ''.join(pL)
    
def filter_01(s):
    return [c for c in s if c in '01']

def stringToIntList(s):
    L = s.strip().split()
    return [int(c) for c in L]

def get4BitDict():
    D = dict()
    for i in range(16):
        b = bin(i)[2:].zfill(4)
        D[b] = i
    return D

def shiftLeft(L, n=1):
    return L[n:] + L[:n]
    
def bstrXOR(c,d):
    if c == '0' and d == '0':  return '0'
    if c == '1' and d == '1':  return '0'
    return '1'

# XOR [int] -> int
def reducingXOR(word):
    result = 0
    for b in word:
        result = result ^ b
    return result

# a single word is 4 bytes
def xorTwoWords(w1,w2):
    return [m^n for m,n in zip(w1,w2)]
    
# four words of 4 bytes each
def xorWordLists(L1,L2):
    rL = list()
    for w1,w2 in zip(L1,L2):
        rL.append(xorTwoWords(w1,w2))
    return rL

# we're using msg and key input as strings of 01

def convertHexKeyInput(h):
    data = bytearray.fromhex(h)
    L = [int(b) for b in data]
    s = ''.join([bin(n)[2:].zfill(8) for n in L])
    ret = pchunks(s, SZ=4, ONELINE = 8)
    return ret

def convertToHexOutput(s):
    chunks = s.strip().split()
    D = get4BitDict()
    hexL = [hex(D[b])[2:] for b in chunks]
    return ''.join(hexL)
