from aes_info import AES_Sbox_encrypt as SE
from aes_info import AES_Sbox_decrypt as SD
import fmt

def sub_bytes(L):
    print("sub_bytes")
    result = [SE[n] for n in L]
    fmt.show(result)
    return result

def inv_sub_bytes(L):
    print("sub_bytes")
    result = [SD[n] for n in L]
    fmt.show(result)
    return result
