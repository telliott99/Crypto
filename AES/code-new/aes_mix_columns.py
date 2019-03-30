from gmath import gmultiply as gm
from gmath import xor_reduce
import fmt

def mix_one_column(sL):
    a,b,c,d = sL     
    # 2, 3, 1, 1
    # 1, 2, 3, 1
    # 1, 1, 2, 3
    # 3, 1, 1, 2
    m = xor_reduce([gm(2,a), gm(3,b),      c,       d  ])
    n = xor_reduce([     a , gm(2,b), gm(3,c),      d  ])
    p = xor_reduce([     a ,      b,  gm(2,c), gm(3,d) ])
    q = xor_reduce([gm(3,a),      b,       c,  gm(2,d) ])
    return [m,n,p,q]

def mix_columns(L):
    print("mix_columns")
    # first four values
    f = mix_one_column
    rL = f(L[:4])
    rL.extend(f(L[4:8]))
    rL.extend(f(L[8:12]))
    rL.extend(f(L[12:16]))
    fmt.show(rL)
    return rL

def inv_mix_one_column(sL):
    a,b,c,d = sL     
    # 14 11 13  9
    #  9 14 11 13
    # 13  9 14 11
    # 11 13  9 14
    m = xor_reduce([gm(14,a), gm(11,b), gm(13,c),  gm(9,d) ])
    n = xor_reduce([ gm(9,a), gm(14,b), gm(11,c), gm(13,d) ])
    p = xor_reduce([gm(13,a),  gm(9,b), gm(14,c), gm(11,d) ])
    q = xor_reduce([gm(11,a), gm(13,b),  gm(9,c), gm(14,d) ])
    return [m,n,p,q]

def inv_mix_columns(L):
    print("inv_mix_columns")
    # first four values
    f = inv_mix_one_column
    rL = f(L[:4])
    rL.extend(f(L[4:8]))
    rL.extend(f(L[8:12]))
    rL.extend(f(L[12:16]))
    fmt.show(rL)
    return rL

def test():
    pass
    
if __name__ == "__main__":
    test()