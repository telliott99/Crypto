import aes_key_expand
from gmath import gmultiply as gm
from gmath import xor, xor_reduce
import fmt
from aes_sub_bytes import inv_sub_bytes
from aes_shift_rows import inv_shift_rows
from aes_mix_columns import inv_mix_columns

def add_round_key(L, kL):
    # just an XOR with the key
    print("add_round_key")
    result = xor(L,kL)
    fmt.show(result)
    return result
    
#------------------------------------------

def do_round0(L, kL0):
    print('round 0')
    fmt.show(L, 'state')
    fmt.show(kL0, 'keyL0')
    result = add_round_key(L, kL0)
    fmt.show(result, 'result of round 0')
    print('-'*30)
    return result
    
def decrypt_round(L, kL, n):
    L = inv_shift_rows(L)
    L = inv_sub_bytes(L)
    L = add_round_key(L, kL[n])
    if not n == 10:
        L = inv_mix_columns(L)
    return L

def do_round(L, keyL, n):
    print('round %d' % n)
    fmt.show(L, 'state')
    fmt.show(keyL[n], 'keyL[%d]' % n)
    result = decrypt_round(L, keyL, n)
    fmt.show(result, 'result of round %d' % n)
    print('-'*30)
    return result

def decrypt(k,ctx):
    L = [ord(c) for c in k]
    keyL = aes_key_expand.get_keys(L)
    # reverse!
    keyL = list(reversed(keyL))
    
    L = [int(h,base=16) for h in ctx.strip().split()]
    print("ciphertext: %s" % ctx)
    print("keytext  : %s" % k)
    
    fmt.show(keyL[0], 'key:')
    L = do_round0(L, keyL[0])
    
    for n in range(1,11):
        L = do_round(L, keyL, n)
        
    print("plaintext:")
    pL = [str(n).rjust(3) for n in L]
    result = ' '.join(pL)
    print(result)
    pL = [hex(n)[2:].zfill(2) for n in L]
    print(' ' + '  '.join(pL))
    
    return L

#------------------------------------------

if __name__ == "__main__":

    k = "Thats my Kung Fu"
    ctx = "29 c3 50 5f 57 14 20 f6 40 22 99 b3 1a 02 d7 3a"
    result = decrypt(k,ctx)
    print(''.join([chr(n) for n in result]))
    

