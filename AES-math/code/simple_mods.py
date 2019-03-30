import operator

def fmt_table(L,ju=3):
    rL = list()
    for sL in L:
        pL = [str(e).rjust(ju) for e in sL]
        rL.append(''.join(pL))
    return '\n'.join(rL) + '\n'

def test(n,op):
    L = list(range(n))
    rL = list()
    for i in L[1:]:
        sL = [i, '|']
        for j in L:
            sL.append((op(i,j)) % n)
        rL.append(sL)
    return rL
        
for i in range(5,16):
    print(str(i).rjust(3))
    #print(fmt_table(list(range(i))))
    rL = test(i, operator.mul)
    print(fmt_table(rL))
