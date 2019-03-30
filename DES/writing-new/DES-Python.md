#### Python 3 module PyCrypto

```
pip3 install pycrypto
```

**commands**:

```
from Crypto.Cipher import DES

k =  b'\x0e\x32\x92\x32\xea\x6d\x0d\x73'
iv = b'\x00'*8
p =  b'\x87'*8
o = DES.new(k,DES.MODE_CBC,iv)
c = o.encrypt(p)
c
o.decrypt(c)
```

**output**

```
>>> c
b'\x00\x00\x00\x00\x00\x00\x00\x00'
>>> o.decrypt(c)
b'\x87\x87\x87\x87\x87\x87\x87\x87'
>>>
```

