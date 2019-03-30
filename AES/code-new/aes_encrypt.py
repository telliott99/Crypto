import fmt
from gmath import xor
import aes_key_expand
import aes_utils as ut
from aes_sub_bytes import sub_bytes
from aes_shift_rows import shift_rows
from aes_mix_columns import mix_columns


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
    
def round(L, kL, n):
    L = sub_bytes(L)
    L = shift_rows(L)
    if not n == 10:
        L = mix_columns(L)
    L = add_round_key(L, kL[n])
    return L

def do_round(L, keyL, n):
    print('round %d' % n)
    fmt.show(L, 'state')
    fmt.show(keyL[n], 'keyL[%d]' % n)
    result = round(L, keyL, n)
    fmt.show(result, 'result of round %d' % n)
    print('-'*30)
    return result

def encrypt(k,p):
    print("plaintext: %s" % p)
    print("keytext  : %s" % k)
    
    L = ut.convert(k)
    print("key as hex:")
    print(ut.printable(L))
    keyL = aes_key_expand.get_keys(L)
    
    L = ut.convert(p)
    print("plaintext as hex:")
    print(ut.printable(L))
        
    fmt.show(keyL[0], 'key:')
    L = do_round0(L, keyL[0])
    for n in range(1,11):
        L = do_round(L, keyL, n)
        
    print("ciphertext:")
    pL = [str(n).rjust(3) for n in L]
    print(' '.join(pL))
    pL = [hex(n)[2:].zfill(2) for n in L]
    result = ' ' + '  '.join(pL)
    print(result)
    return result

#------------------------------------------

if __name__ == "__main__":

    k = "Thats my Kung Fu"
    p = "Two One Nine Two"
    ctx = encrypt(k,p)

