import utils as ut
import info

# a key is really a keyList
# ['0', '1', '0' ..        of length __
# schedule IP

# no drops in this one
def do_2a(mL):
    rL = list()
       
    L = ut.stringToIntList(info.IP)
    # convert to 0-based indexing
    sched = [n-1 for n in L]

    for i in range(len(mL)):
        j = sched[i]
        rL.append(mL[j])
    return rL

def test_2a():
    input = info.msg
    kL = ut.filter_01(input)

    result = do_2a(kL)
    print ut.pchunks(
        result, SZ=8, ONELINE=4) + '\n'

# test_2a()