import fmt

def shift_rows(L):
    print("shift_row")
    # L displayed *by columns*
    iL = [0,5,10,15,4,9,14,3,
          8,13,2,7,12,1,6,11]
    rL =  [L[i] for i in iL]
    fmt.show(rL)
    return rL

def inv_shift_rows(L):
    print("inverse shift_rows")
    #print("input:")
    #fmt.show(L)
    #print("output:")
    # L displayed *by columns*
    # original
    # iL= [0,  5, 10, 15,  4,  9,  14,  3,
    #      8, 13,  2,  7, 12,  1,   6, 11]

    iL =  [0, 13, 10,  7,  4,  1,  14, 11,
           8,  5,  2, 15, 12,  9,   6,  3]
    rL =  [L[i] for i in iL]
    fmt.show(rL)
    return rL
