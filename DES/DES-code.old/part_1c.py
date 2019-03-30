import utils as ut
import info

# a key is really a keyList
# ['0', '1', '0' ..        of length __
# schedule PC2
    
def do_1c(kL):
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

def test_1c():
    input = info.K16_7.strip().split('\n')
    master = [ut.filter_01(kL) for kL in input]
    rL = list()
    
    for kL in master:
        rL.append(do_1c(kL))
    print_test_results(rL)
    return rL

def print_test_results(rL):
    print '16 permuted keys:'  # 48 bits
    for kL in rL:
        print ut.pchunks(
            kL, SZ=6, ONELINE=8)
    
if __name__ == "__main__":
    test_1c()

# for output see K16_6 in info.py