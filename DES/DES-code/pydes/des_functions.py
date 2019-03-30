try:
    from pydes import utils as ut
    from pydes import info
    
except ImportError:
    import platform
    t = (platform.python_version(),__name__)
    print("triggered ImportError:\n  Python%s\n  %s" % t)
    
    import utils as ut
    import info 

def first_permutation(kL):
    rL = list()
    
    L = ut.stringToIntList(info.PC1)
    # convert to 0-based indexing
    sched = [n-1 for n in L]

    for i in range(len(kL)):
        if i % 8 == 7:
            continue
        j = sched[i]
        rL.append(kL[j])
    return rL

#----------------------------------------

def shift_by_schedule(input):
    sL =  info.shifts
    rL = list()    
    tmp = input
    # we drop C0 and D0
    for i in range(len(sL)):
        tmp = ut.shiftLeft(tmp, n=sL[i])
        rL.append(tmp[:])
    return rL
    
def get_shifted_key_lists(C0,D0):
    cL = shift_by_schedule(C0)
    dL = shift_by_schedule(D0)
    # reform the wholes
    rL = [c+d for c,d in zip(cL,dL)]
    return rL

#----------------------------------------

def second_permutation(kL):
    rL = list()  
    # PC-2 uses only 48 bits
    # every 7th bit is discarded
    
    L = ut.stringToIntList(info.PC2)
    # convert to 0-based indexing
    sched = [n-1 for n in L]
    
    for i in range(len(kL)):
        if i % 7 == 6:
            continue
        j = sched[i]
        rL.append(kL[j])
    return rL

#----------------------------------------

def message_permutation(mL):
    rL = list()
       
    L = ut.stringToIntList(info.IP)
    # convert to 0-based indexing
    sched = [n-1 for n in L]

    for i in range(len(mL)):
        j = sched[i]
        rL.append(mL[j])
    return rL


#----------------------------------------

# calculation of f

# a key is really a keyList
# ['0', '1', '0' ..        of length __

# no drops in this one!

# step 2a i:  expand
def expand(Rn):
    '''
    Expand 32-bit Rn to 48 bits by repeating bits
    using the selection table E_TABLE
    '''
    L = ut.stringToIntList(info.E_TABLE)
    # convert to 0-based indexing
    sched = [n-1 for n in L]
    rL = list()
    for i in sched:
        rL.append(Rn[i])
    return rL
    
def use_S_boxes(xL):
    '''
    Input is a 48-bit key
    Break key into 8 groups of 6 bits
    Look-up in S1..S8 using 6 bits as the address
    Each value is a 4-bit number
    Return a 32-bit result
    '''
    # print 'xL: ', ut.pchunks(xL, SZ=6, ONELINE=8)
    
    sL = [info.S1, info.S2, info.S3, info.S4,
          info.S5, info.S6, info.S7, info.S8 ]
    sL = [ut.stringToIntList(s) for s in sL]
    
    cL = ut.chunks(xL, n=6)
    cL = [''.join(e) for e in cL]
    cD = ut.get4BitDict()
    rD = { '00': 0, '01': 1, '10': 2, '11': 3 }
    
    rL = list()
    
    for S, chunk in zip(sL, cL):
        
        # weird way to break up the 6-bit value
        row = rD[chunk[0] + chunk[-1]]
        col = cD[chunk[1:5]]
        
        # system is already 0-based:  '00' = row 1 (1-based)
        index = ((row * 16) + col)
        val = S[index]
        b = bin(val)[2:].zfill(4)
        
        # print row, col, index, val, b
        rL.append(b)
    return list(''.join(rL))
    
def f_permute(fL):
    # print 'fL: ', ut.pchunks(fL, SZ=4, ONELINE=8)  # 32 bits

    L = ut.stringToIntList(info.P)
    # convert to 0-based indexing
    sched = [n-1 for n in L]
    
    rL = list()
    for i in sched:
        rL.append(fL[i])
    return rL
        
# just working one round so far
def one_round_2b(L0, R0, kL):
    eL = expand(R0)
    # print 'eL: ', ut.pchunks(eL, SZ=6, ONELINE=8)  # 48 bits
    # print 'kL: ', ut.pchunks(kL, SZ=6, ONELINE=8)

    # step 2a ii:  XOR with key
    xL = [ut.bstrXOR(c,d) for c,d in zip(kL,eL)]
    # print 'xL: ', ut.pchunks(xL, SZ=6, ONELINE=8)
    
    # step 2a iii:  use S boxes
    # xL contains 16 48-bit keys
    fL = use_S_boxes(xL)
    # print 'fL: ', ut.pchunks(fL, SZ=4, ONELINE=8)
    
    pmL = f_permute(fL)
    # print 'pmL: ', ut.pchunks(pmL, SZ=4, ONELINE=8)
    
    R1 = [ut.bstrXOR(c,d) for c,d in zip(L0,pmL)]
    
    '''
    L1 = R0
    R1 = L0 + f(R0,K0)
    '''
    return R1
    

# input is a list of 16 keyLists 
def do_multiple_rounds_2b(mL, input):
    L = mL[:32]
    R = mL[32:]
    
    for i in range(16):
        # get the ith key
        kL = ut.filter_01(input[i])
        nextR = one_round_2b(L, R, kL)
        L = R
        R = nextR
        
    L16, R16 = L, R
    # print 'L16: ', ut.pchunks(L16, SZ=4, ONELINE=8)
    # print 'R16: ', ut.pchunks(R16, SZ=4, ONELINE=8)
    
    # reverse order
    rL = R16 + L16
    # print 'rL: ', ut.pchunks(rL, SZ=8, ONELINE=8)
    return rL

def final_step(input):
    # print 'rL: ', ut.pchunks(eL, SZ=8, ONELINE=8)  # 64 bits
    
    # another permutation
    L = ut.stringToIntList(info.IP_inv)
    # convert to 0-based indexing
    sched = [n-1 for n in L]
    
    rL = list()
    for i in sched:
        rL.append(input[i])
    return rL