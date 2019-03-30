#### DES

I previously worked out how to implement DES in Python.  

I was going to re-implement it (it seemed easier than parsing my old code), but then I resisted the impulse.  I just went back and worked with what I have.

My writeup from before of the detailed steps is [here](writing-old/DES3-ECB-me.md).

The code is in the ``DES-code`` directory, and it still works with Python 2.

From the Github/DES directory

```
> cd DES-code
> python
..
>>> from pydes import des
>>> key = '133457799BBCDFF1'
>>> msg = '0123456789abcdef'
>>> ctx = des(msg,key)
>>> ctx
'85e813540f0ab405'
>>> des(ctx,key,mode="decrypt")
'0123456789abcdef'
>>>
```

I am going to make this work with Python 3 here.  

But first, some new early exploration:

- a [first example](writing-new/DES-openssl.md) of ``openssl`` in DES CBC mode
- [write](writing-new/write-bytes.md) bytes to disk:  ``echo`` or ``printf``
- [Python](writing-new/DES-python.md) invocation of DES
- discussion of [padding](intro/openssl-padding.md) for ``openssl`` in DES mode
- a [bigger example](writing-new/DES-openssl-2.md) of ``openssl`` DES

[Here](sources/The DES Algorithm Illustrated.pdf) is an extensive discussion of DES ([web source](http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm)), and Wikipedia also has a long [article](https://en.wikipedia.org/wiki/Data_Encryption_Standard).

#### Python 3

The only problem I ran into was with imports.  My writeup is [here](DES-code/python3-changes.txt).
