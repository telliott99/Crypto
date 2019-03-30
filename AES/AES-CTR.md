Here is an example of AES running in CTR mode (pycrypto).

```python
from Crypto.Cipher import AES
import os

def f(L):
    hL = [hex(ord(c))[2:].zfill(2) for c in L]
    return ''.join(hL)
    
key = os.urandom(16)
iv = os.urandom(16)
print ' k', f(key)
print 'iv', f(iv)

cipher = AES.new(key, AES.MODE_CTR, 
                 counter = lambda: iv)

s = 'aaa'
print ' s', s

ctx = cipher.encrypt(s)
print ' c', f(ctx)
print ' p', f(cipher.decrypt(ctx))
```

output:

```bash
> python aes_ctr_ex.py 
 k d167143c91505de7239e913c3273c2d2
iv e154478320cb939784c400b12a20af10
 s aaa
 c e682c6
 p eed48a
>
```