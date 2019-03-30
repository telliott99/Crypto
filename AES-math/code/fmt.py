# skip_first value (None) for log and antilog tables

def fmt(L, hex_fmt=False, 
           skip_first=False): 
    if hex_fmt:
        pL = [hex(n)[2:].zfill(2) for n in L]
    else:
        pL = [str(i).rjust(3) for i in L]
        
    n = 16
    rL = list()
    
    # we have one space between items of length 2 or 3
    if skip_first:
        if hex_fmt:
            rL.append(' '*3 + ' '.join(pL[:15]))
        else:
            rL.append(' '*4 + ' '.join(pL[:15]))
        pL = pL[15:]
        
    while pL:
        rL.append(' '.join(pL[:n]))
        pL = pL[n:]
    return '\n'.join(rL)
