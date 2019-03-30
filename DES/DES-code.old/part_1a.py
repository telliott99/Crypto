import utils as ut
import info

# a key is really a keyList
# ['0', '1', '0' ..        of length __
# schedule PC1
    
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

def test_1a():
    input = info.key
    kL = ut.filter_01(input)
        
    result = do_1a(kL)
    print_test_results(kL, result)

def print_test_results(kL, result):
    # 64 bits
    print 'key:\n', ut.pchunks(
        kL, SZ=8, ONELINE=4) + '\n'
    
    # 56 bits
    print 'mod key:\n', ut.pchunks(
        result, SZ=7, ONELINE=4)
        
    return result
    
if __name__ == "__main__":
    test_1a()

'''
> python part_1a.py 
key:
00010011 00110100 01010111 01111001
10011011 10111100 11011111 11110001

mod key:
1111000 0110011 0010101 0101111
0101010 1011001 1001111 0001111
>

compare to article's K+:
1111000 0110011 0010101 0101111
0101010 1011001 1001111 0001111
'''
