#### Inversion

Decryption is the inverse of encryption in the sense that 

```
decrypt(encrypt(p)) == p
```

For the S-boxes, it's pretty easy.  These are lookup tables that map each byte in [0-255] to another byte.

They are set up so that S-decrypt is the inverse of S-encrypt.  For example in S-encrypt on line 1 we have:

```
 99 124 119 123 242 107 111 197  48   1 ..
```

This maps the integer 9 to the integer 1.  In S-decrypt we have

```
  82   9 ..
 124 227 ..
  84 123 ..
   8  46 ..
```

that entry on the top row maps 1 back to 9.  Similarly, the first table maps 8 to 48 (see above), and the second table maps 48 back to 8 as shown on the last row.

#### matrix multiplication

I messed around with matrix multiplication a bit and found some interesting patterns, but the results were not correct.  

Even for small numbers it can be important to use gmultiply rather than old fashioned multiplication.  I wrote a routine (in matrix.py) which multiplies matrices using Galois field math.

If you do that the pattern is clear:

```
2 3 1 1    2 3 1 1     14 11 13  9
1 2 3 1    1 2 3 1  =   9 14 11 13
1 1 2 3    1 1 2 3     13  9 14 11
3 1 1 2    3 1 1 2     11 13  9 14
```

and

```
2 3 1 1    14 11 13  9      1  0  0  0
1 2 3 1     9 14 11 13  =   0  1  0  0
1 1 2 3    13  9 14 11      0  0  1  0
3 1 1 2    11 13  9 14      0  0  0  1
```

Here is part of the code:

```
def mmul(a,b):
    b = zip(*b)
    rL = list()
    for i in range(4):
        sL = list()
        for j in range(4):
            n = dot(a[i],b[j])
            sL.append(n)
        rL.append(sL)
    return rL
```

We use Peter Norvig's [trick](https://norvig.com/python-iaq.html) (search for "transpose") to transpose *b*.

And here is the other part:

```
def xor(L):
    r = 0
    for n in L:
        r = r ^ n
    return r

def dot(L1,L2):
    rL = [gm(x,y) for x,y in zip(L1,L2)]
    return xor(rL)
```

The first part could be done with ``reduce``:

```
>>> import operator
>>> reduce(operator.xor,[1,2,3])  
0
>>>
```

and the second part could be done with ``map``:

```

```