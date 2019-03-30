# the padded message block
# SHA-256 uses 1024 bits as 16 @ 64-bit words

def compute_pad(iL):
    # block size in bits
    N = 1024  
    SZ = N/8  # 128 bytes
    
    # msg size in bytes
    n = len(iL)
    
    # the length at the end must be
    # represented in 128 bits = 16 bytes
    
    # how many zero bytes do we need between?
    # 128 minus 16 bytes 
    # + 1 byte plus the n msg bytes
    
    extra = SZ - ((n + 17) % SZ)
    # print 'extra', extra
   
    # save the extra byte starting with '1'
    iL.append(128)
    # then the zero bytes
    iL += [0] * extra
    
    # and finally 8 bytes with the length in *bits*
    b = bin(n*8)[2:]
    e = '0' * (128 - len(b))
    b = e + b
    
    for i in range(0,len(b),8):
        sub = b[i:i+8]
        m = int('0b' + sub, 2)
        iL.append(m)

    return iL

def pad_data(iL):
    iL = compute_pad(iL)
    
    # problem now is to convert a list of single bytes 
    # to a list of 64-bit integer values
    
    mL = list()
    
    '''
    for i in range(0,len(iL),8):
        v =  256**7 * iL[i]
        v += 256**6 * iL[i+1]
        v += 256**5 * iL[i+2]
        v += 256**4 * iL[i+3]
        v += 256**3 * iL[i+4]
        v += 256**2 * iL[i+5]
        v += 256**1 * iL[i+6]
        v += iL[i+7]
        print 'v', v
        mL.append(v)
    '''
    
    for i in range(0,len(iL),8):
        sL = iL[i:i+8]
        ssL = [hex(e)[2:].zfill(2) for e in sL]
        v = int(''.join(ssL),16)
        mL.append(v)
            
    return mL
