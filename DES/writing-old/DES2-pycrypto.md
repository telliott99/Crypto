Here is an example from **s1n7**

```python
from Crypto.Cipher import AES
k = "YELLOW SUBMARINE"
cipher = AES.new(k, AES.MODE_ECB)

import utils as ut
data = ut.readData('s1n7.data.bin','rb')
p = cipher.decrypt(data)

>>> for line in p.strip().split('\n'):
...     print line
... 
I'm back and I'm ringin' the bell 
A rockin' on the mike while the fly girls yell 
In ecstasy in the back of me 
Well that's my DJ Deshay cuttin' all them Z's 
Hittin' hard and the girlies goin' crazy 
Vanilla's on the mike, man I'm not lazy. 
```

<hr>

That example is AES, though it is ECB.  One difference is that AES uses 128-bit (16-byte) keys, such as 'YELLOW_SUBMARINE'.

How about DES?  DES uses 8-bit keys.

One of our 8 bit examples from the DES tutorial was

```
msg:  \x87 * 8
key:  0E329232EA6D0D73
ctx:  0000000000000000
```

```python
>>> from Crypto.Cipher import DES
>>> k = '0E329232EA6D0D73'
>>> cipher = DES.new(k, DES.MODE_ECB)
>>> ValueError: Key must be 8 bytes long, not 16
```

A couple notes:  the [docs](https://www.dlitz.net/software/pycrypto/api/current/) say the default mode for DES.new is MODE_ECB.

And the key is a byte string

Try this:

```python
>>> k = '\x0e\x32\x92\x32\xea\x6d\x0d\x73'
>>> cipher = DES.new(k)
>>> cipher.block_size
8
>>> data = '\x87' * 8
>>> data
'\x87\x87\x87\x87\x87\x87\x87\x87'
>>> p = cipher.encrypt(data)
>>> p
'\x00\x00\x00\x00\x00\x00\x00\x00'
>>> 
```

Or from a file:

``` python
>>> import utils as ut
>>> data = ut.readData('m87.bin')
>>> data
'\x87\x87\x87\x87\x87\x87\x87\x87'
>>> p = cipher.encrypt(data)
>>> p
'\x00\x00\x00\x00\x00\x00\x00\x00'
>>>
```

Compare with:

```bash
> openssl des-ecb -e -nopad -K "0E329232EA6D0D73" -in m87.bin | xxd -p
0000000000000000
>
```

Recall that to generate binary data from a hex string in Python we can do:

```
>>> h = '0E329232EA6D0D73'
>>> h.decode('hex')
'\x0e2\x922\xeam\rs'
>>>
```
Here Python has printed ``e`` as the ASCII equivalent for decimal ``50``, which is hex ``32``.

