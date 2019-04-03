import sys
from aes_encrypt import encrypt
from aes_decrypt import decrypt
import aes_utils as ut

try:
    p = sys.argv[1]
except IndexError:
    p = "Two One Nine Two"  
p = ut.pad(p)
    
#-------------------
    
try:
    k = sys.argv[2]
except IndexError:
    k = "Thats my Kung Fu"
k = ut.pad_key(k)
    
#-------------------

# p = "strawberryfields"
hex_ctx = encrypt(k,p)
result = decrypt(k,hex_ctx)
print(''.join([chr(n) for n in result]))
