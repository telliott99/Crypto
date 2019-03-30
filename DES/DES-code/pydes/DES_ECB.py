try:
    from pydes import utils as ut
    from pydes import info
    from pydes.des_functions import *
    
except ImportError:
    import platform
    t = (platform.python_version(),__name__)
    print("triggered ImportError:\n  Python%s\n  %s" % t)
    
    import utils as ut
    import info
    from des_functions import *

# modified to use hex input

def des(msg, key, mode = 'encrypt'):
    key = ut.convertHexKeyInput(key)
    msg = ut.convertHexKeyInput(msg)
   
    # 1a
    kL = ut.filter_01(key)
    result_1a = first_permutation(kL)
    # print "1a:\n", ut.pchunks(result_1a, SZ=7, ONELINE=8)
    
    # 1b
    C0 = result_1a[:28]
    D0 = result_1a[28:]
    # print ut.pchunks(C0, SZ=7, ONELINE=8)
    # print ut.pchunks(D0, SZ=7, ONELINE=8)
    rL = get_shifted_key_lists(C0,D0)
    
    # for output to match see K16_7 in info.py
    # for kL in rL:
        # print ut.pchunks(kL, SZ=7, ONELINE=8)
    
    # 1c
    master = rL[:]
    rL = list()
    
    for kL in master:
        rL.append(second_permutation(kL))
        
    # need another label here, this is a list of lists
    kL = rL[:]
    # for output to match see K16_6 in info.py
    # for kL in rL:
        # print ut.pchunks(kL, SZ=6, ONELINE=8)
    
    # 2a
    mL = ut.filter_01(msg)
    mL = message_permutation(mL)
    # print "2a:\n", ut.pchunks(
        # mL, SZ=8, ONELINE=4) + '\n'
        
    # this is all it takes
    if mode == 'decrypt': 
        kL.reverse()
    
    # 2b
    result = do_multiple_rounds_2b(mL, kL)
    final_result = final_step(result)
    
    ret = ut.pchunks(final_result, SZ=4, ONELINE=16)
    # print ret
    return ut.convertToHexOutput(ret)    

if __name__ == "__main__":
    key = '133457799BBCDFF1'
    msg = '0123456789abcdef'
    
    # default is encode
    ctx = des(msg, key)
    print('ctx: %s' % ctx)
    
    ptx = des(ctx, key, mode = 'decrypt')
    print('ptx: %s' % ptx)
    
'''
> python DES_ECB.py
ctx: 85e813540f0ab405
ptx: 0123456789abcdef
>
'''