import aes_utils as ut

def formatTable(L, mode='int'):
    def getHex(n):
        return hex(n)[2:].zfill(2)
    LEN = 16
    rL = list()
    
    # since 0 and 1 lack inverses skip for both
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

#----------------------------------------------

data = ut.readData('log.int.txt')
logL = [int(s) for s in data.strip().split()]
logL.insert(0, None)
rL = [None, 1]

for i in range(2,256):
    log1 = logL[i]
    delta = 255 - log1
    L = list()
    for j in range(1,256):
       if logL[j] == delta:
           L.append(j)
    assert len(L) == 1
    rL.append(L[0])

print formatTable(rL, mode='hex')