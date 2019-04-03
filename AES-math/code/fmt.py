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


def fmt_matrix(L):
    def line_fmt(L,n):
        pL = [str(i).rjust(n) for i in L]
        return ' '.join(pL)
    rL = list()
    for row in L:
        rL.append(line_fmt(row,2))
    return '\n'.join(rL) + '\n'

def fmt_matrix_mul(*L):
    L = list(L)
    sep = '    '
    def l_adjust(blob):
        sL = blob.split('\n')
        w = max([len(e) for e in sL])
        sL = [e.ljust(w) for e in sL]
        return sL
        
    def meld(L1,L2):
        while len(L1) < len(L2):
            n = len(L1[0])
            L1.append(" " * n)
        return [sep.join([s1,s2]) for s1,s2 in zip(L1,L2)]
         
    pL = l_adjust(L.pop(0))
    while L:
        next = l_adjust(L.pop(0))
        pL = meld(pL,next)
    return '\n'.join(pL)
        
if __name__ == "__main__":
    s1 = '1 2 3\n4 5 6\n7 8 9\n'
    s2 = '11 12 13\14 15 16\n17 18 19'
    print(fmt_matrix_mul([s1,s2]))
        
    
