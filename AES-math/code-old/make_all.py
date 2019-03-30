# python make_all.py > all.x3tables.txt

import aes_utils as ut

# special cases:
# 256 values but None is first one:  logs, inv
# deal with None in getString

def getString(n, mode = 'int'):
    if n == None:
        if mode == 'hex':
            return '  '
        return '   '
    if mode == 'int':
        return str(n).rjust(3)
    if mode == 'hex':
        return hex(n)[2:].zfill(2)

def formatTable(L, mode='hex', LEN = 16):
    rL = list()
    for i in range(0, len(L), LEN):
        line = L[i:i+LEN]
        if mode == 'hex':
            sL = [getString(n, mode) for n in line]
        elif mode == 'int':
            sL = [getString(n) for n in line]
        rL.append(' '.join(sL))
    return '\n'.join(rL) + '\n'

# ------------------------------------------

def normalized(n):
    #  mod 100011011 but only if
    # n >= 100000000
    if n < 256:
        return n
    return (n % 256) ^ 27

def times2(n):
    r = n << 1
    return normalized(r)

def times3(n):
    r = (n << 1) ^ n
    return normalized(r) 

def field_generator(f):
    n = 1
    while True:
        yield n
        n = f(n)

def makeExps():
    g = field_generator(times3)
    expL = [g.next() for i in range(256)]
    return expL

# ------------------------------------------

def makeLogs(expL):
    logL = [None] * 256
    for i in range(256):
        v = expL[i]
        logL[v] = i
    logL[1] = 0
    return logL
    
def makeInverses(logL):
    rL = list()
    for i in range(2,256):
        sL = list()
        log1 = logL[i]
        delta = 255 - log1
        for j in range(1,256):
           if logL[j] == delta:
               sL.append(j)
        assert len(sL) == 1
        rL.append(sL[0])
    rL.insert(0, 1)
    rL.insert(0, None)
    return rL

# ------------------------------------------

def multiplyUsingLogs(x,n):
    log1 = logL[x]
    log2 = logL[n]
    log = (log1 + log2)
    # 255 is counter-intuitive!
    if log > 255:
        log -= 255
    return expL[log]


expL = makeExps()
print formatTable(expL)

logL = makeLogs(expL)
print formatTable(logL)

invL = makeInverses(logL)
print formatTable(invL)

