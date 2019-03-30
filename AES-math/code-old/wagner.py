from random import choice as ch
import random

random.seed(133)

# n lists with SZ unique values
# high values first
def random_int_lists(num, SZ):
    R = range(8)
    rL = list()
    for n in range(num):
        sL = [ch(R) for i in range(SZ)]
        sL = list(set(sL))
        sL.sort(reverse=True)
        rL.append(sL)
    return rL

# input is a sorted list [13, 9, 3] 
# unique values variable number
# output is always the same length
def format(inL):
    L = inL[:]
    L.reverse()
    pL = list()
    # count down to make pop more efficient
    for i in range(15,-1,-1):
        if L and  L[-1] == i:
            pL.append(str(i))
            L.pop()
        elif i > 9:
            pL.append('  ')
        else:
            pL.append(' ')
    return ' '.join(pL)

# two or more lists of values 
# as a string from format
def stringXOR(sL):
    # all the same length in print chars
    rL = list()
    for i in range(len(sL[0])):
        cL = [s[i] for s in sL]
        cL = [c for c in cL if not c == ' ']
        if len(cL) % 2 == 0:
            rL.append(' ')
        else:
            rL.append(cL[0])
    return ''.join(rL)
    
def test_format():
    L = random_int_lists(4,7)
    pL = [format(sL) for sL in L]
    print '\n'.join(pL)
    
    print stringXOR(pL)
    
# test_format()

#-----------------------------------------------
def wagner(xL, yL):
    sx = ','.join([str(n) for n in xL])
    sy = ','.join([str(n) for n in yL])
    rL1 = list()
    rL2 = list()
    for y in yL:
        sL = [x + y for x in xL]
        tL = ('= %d' % y) + ' * (' + sx + ')'
        rL1.append(sL)
        rL2.append(tL)
    print sx, '*', sy
    print '-' * (len(sx + sy) + 3)
    return rL1, rL2

def run_wagner(xL, yL):
    rL, tL = wagner(xL, yL)
    pL = [format(sL) for sL in rL]
    for s,t in zip(pL,tL):
        print s, t
    return pL

def modulus(s):
    mL = [8,4,3,1,0]
    pm = ','.join([str(n) for n in mL])
    L = [int(d) for d in s.split()]
    v = s
    print
    print s
    while L and L[0] > 7:
        d = L[0] - 8
        ms = format([m + d for m in mL])
        #print v
        print ms, ('= %d' % d) + ' * (' + pm + ')'
        print
        v = stringXOR([v,ms])
        print v + '   XOR'
        #print '-' * 60
        L = [int(d) for d in v.split()]

def run_test(xL, yL):
    pL = run_wagner(xL,yL)
    sx = stringXOR(pL)
    print sx + '   XOR\n'
    modulus(sx)

def hexForList(L):
    rL = list()
    first = 0
    if 7 in L:  first += 8
    if 6 in L:  first += 4
    if 5 in L:  first += 2
    if 4 in L:  first += 1
    h1 = hex(first)[2:]
    second = 0
    if 3 in L:  second += 8
    if 2 in L:  second += 4
    if 1 in L:  second += 2
    if 0 in L:  second += 1
    h2 = hex(second)[2:]
    return h1 + h2

def random_test():
    xL,yL = random_int_lists(2,7)
    run_test(xL, yL)
    print xL, hexForList(xL)
    print yL, hexForList(yL)
    print
    print

def test_MI():
    xL = [6,4,1,0]
    yL = [7,6,3,1]
    pL = run_wagner(xL,yL)
    sx = stringXOR(pL)
    print sx + '   XOR'
    modulus(sx)
    print xL, hexForList(xL)
    print yL, hexForList(yL)

random_test()
test_MI()


        