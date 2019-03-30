# the padded message block
# SHA-1 uses 512 bits as 16 @ 32-bit words

def compute_pad(iL):
    # block size in bits
    N = 512  
    SZ = N/8  # 64 bytes
    
    # msg size in bytes
    n = len(iL)
    # print 'n', n
    
    # the length at the end must be
    # represented in 64 bits = 8 bytes
    
    # how many zero bytes do we need between?
    # 64 minus
    # 8 bytes + 1 byte plus the n msg bytes
    
    extra = SZ - ((n + 9) % SZ)
    # print 'extra', extra
   
    # save the extra byte starting with '1'
    iL.append(128)
    # then the zero bytes
    iL += [0] * extra
    
    # and finally the 8 bytes with the length in *bits*
    b = bin(n*8)[2:]
    e = '0' * (64 - len(b))
    b = e + b
    for i in range(0,len(b),8):
        sub = b[i:i+8]
        m = int('0b' + sub, 2)
        iL.append(m)

    return iL

def pad_data(iL):
    iL = compute_pad(iL)
    
    # problem now is to convert a list of bytes 
    # to a list of 4-byte values
    
    mL = list()
    for i in range(0,len(iL),4):
        v = 256**3 * iL[i]
        v += 256**2 * iL[i+1]
        v += 256 * iL[i+2]
        v += iL[i+3]
        mL.append(v)
    return mL
