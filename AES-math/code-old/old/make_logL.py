import aes_utils as ut
from random import choice as ch

def formatTable(L, mode='int'):
    def getHex(n):
        return hex(n)[2:].zfill(2)
    LEN = 16
    rL = list()
    
    # since log doesn't have 0 value skip for both
    for i in range(0, len(L), LEN):
        line = L[i:i+LEN]
        if i == 0:  value = line.pop(0)
        if mode == 'hex':
            sL = [getHex(n) for n in line]
        elif mode == 'int':
            sL = [str(n).rjust(3) for n in line]
        if i == 0:
            sL.insert(0,'  ')
        rL.append(' '.join(sL))
    return '\n'.join(rL)

def makeLogs(expL):
    logL = [None] * 256
    for i in range(256):
        v = expL[i]
        logL[v] = i
    logL[1] = 0
    return logL
    

data = ut.readData('exp.int.txt')
expL = [int(s) for s in data.strip().split()]
logL = makeLogs(expL)
print formatTable(logL)
