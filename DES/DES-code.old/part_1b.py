import utils as ut
import info

# a key is really a keyList
# ['0', '1', '0' ..        of length __
    
def shiftLeft(L, n=1):
    return L[n:] + L[:n]

def shift_by_schedule(input):
    sL =  info.shifts
    rL = list()    
    tmp = input
    # we drop C0 and D0
    for i in range(len(sL)):
        tmp = shiftLeft(tmp, n=sL[i])
        rL.append(tmp[:])
    return rL
    
def get_shifted_key_lists(C0,D0):
    cL = shift_by_schedule(C0)
    dL = shift_by_schedule(D0)
    # reform the wholes
    rL = [c+d for c,d in zip(cL,dL)]
    return rL
   
def test_1b():
    input = info.Kplus
    kL = ut.filter_01(input)
    C0 = kL[:28]
    D0 = kL[28:]
    rL = get_shifted_key_lists(C0,D0)
    for kL in rL:
        print ut.pchunks(kL, SZ=7, ONELINE=8)
        
if __name__ == "__main__":
    test_1b()

# for output see K16_7 in info.py