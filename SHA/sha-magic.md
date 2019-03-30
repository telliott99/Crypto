### SHA

In this project, we will have take a look at how hash functions work.

One source I'm following is from [Kak](https://engineering.purdue.edu/kak/compsec/NewLectures/Lecture15.pdf).

Perhaps even better is the official NIST doc [fips180-2.pdf](http://csrc.nist.gov/publications/fips/fips180-2/fips180-2.pdf).

This doc is officially superseded by a subsequent version as well [fips180-4.pdf](http://csrc.nist.gov/publications/fips/fips180-4/fips180-4.pdf), however, the first document has examples that were removed from the later version.

Before we do that, we need to understand how certain *magic* numbers are derived.  

For example, the NIST pdf says (p. 14):

>    For SHA-512, the initial hash value, H(0), shall consist of the following eight 64-bit words, in hex:

```
6a09e667f3bcc908
bb67ae8584caa73b
3c6ef372fe94f82b
a54ff53a5f1d36f1
510e527fade682d1
9b05688c2b3e6c1f
1f83d9abfb41bd6b
5be0cd19137e2179
```

>    These words were obtained by taking roots of the first eight prime numbers.

I struggled to understand what this means.  

Luckily I found an [implementation](https://gmgolem.wordpress.com/2016/04/03/sha-256-initial-hash-derivation-explained-in-ti-nspire) on the web.  Here is that example.  

Suppose we start with the square root of 2.

```
>>> from math import sqrt
>>> r = sqrt(2)
>>> r
1.4142135623730951
>>> n = r * 16
>>> n
22.627416997969522
>>> n = n % 16
>>> hex(int(n))
'0x6'
>>> r = n - int(n)
>>> r
0.6274169979695223
>>>
```

And indeed, the first entry of the table above starts with `6`.   Try another round.

```
>>> r
0.6274169979695223
>>> n = r * 16
>>> n
10.038671967512357
>>> n = n % 16
>>> hex(int(n))
'0xa'
>>> r = n - int(n)
>>> r
0.03867196751235724
>>> 
```

And so it goes.  An important aspect of the built-in math module's `sqrt` is limited precision.  If you use it, you will find the last few digits are off.  

We can do better with the `decimal` module.

[magic1.py](constants/magic1.py)

```
from decimal import *
from math import sqrt

def doOne(n,N):
    n = Decimal(n).sqrt()
    n = sqrt(n)
    pL = list()
    for i in range(N):
        m = (n*16) % 16
        v = int(m)
        n = m - v
        h = hex(v)
        pL.append(h[2])
    return ''.join(pL)

for p in [2,3,5,7,11,13,17,19]:
    print str(p).rjust(2), doOne(p,16)

```

**output**  [magic1.txt](constants/magic1.txt)

```
> python magic.py
 2 6a09e667f3bcc908
 3 bb67ae8584caa73b
 5 3c6ef372fe94f82b
 7 a54ff53a5f1d36f1
11 510e527fade682d1
13 9b05688c2b3e6c1f
17 1f83d9abfb41bd6b
19 5be0cd19137e2179
>
```

In the NIST docs and in [Kak](https://engineering.purdue.edu/kak/compsec/NewLectures/Lecture15.pdf) there are additional magic values which are the "fractional parts of the cube roots of the first eighty prime numbers."

We need the first 80 primes (from [here](primes.utm.edu)) and saved [here](constants/primes80.txt).

[magic2.py](constants/magic2.py)

```
from decimal import *

def cube_root(x):
    return Decimal(x) ** (Decimal(1) / Decimal(3))

def doOne(n,N):
    n = cube_root(n)
    pL = list()
    for i in range(N):
        m = (n*16) % 16
        v = int(m)
        n = m - v
        h = hex(v)
        pL.append(h[2])
    return ''.join(pL)

fn = 'primes.txt'
fh = open(fn,'r')
data = fh.read().strip().split()
primes = [int(e) for e in data]
fh.close()

for p in primes:
    print str(p).rjust(3), doOne(p,16)
```

Part of the output is

```
> python x.py
  2 428a2f98d728ae22
  3 7137449123ef65cd
  5 b5c0fbcfec4d3b2f
...
397 597f299cfc657e2a
401 5fcb6fab3ad6faec
409 6c44198c4a475817
> 
```

This matches Kak (pp 44-45), so far as I checked it.  We write these to files:  [magic1.txt](constants/magic1.txt), and and [magic2.txt](constants/magic2.txt).