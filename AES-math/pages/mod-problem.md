#### Mod problem

To review, we constructed a Galois field called GF(2<sup>8</sup>) by specifying the two operations:

- addition as XOR
- multiplication by multiples 2<sup>n</sup> as bit shifting left by n plus addition
- all of this is mod the irreducible polynomial

``x^8 + x^5 + x^4 + x^2 + x^1 = 256 + 27 = 283``

We used this plus the knowledge that there are primitive elements and that ``0x03`` is one of these to

- generate all 256 elements of the field as powers of ``0x03``
- invert the table of powers into a table of discrete logarithms
- use the logarithms to construct a table of multiplicative inverses

#### Issue with mod operation

The tables are correct according to my source.  

But in testing, I found a problem with the multiplication function I wrote in Python, specifically with the mod part.

It gives the correct answer only as long as the result is small enough.  Here is where we figure that out.

This is the graphical method:

```
0xb6 * 0x53
b6 = 10110110
53 = 01010011

write b6 left-aligned with 1's in 53:
53 = 01010011

      10110110
        10110110
           10110110
            10110110
      --------------
XOR   10011100111010


irreducible polynomial p
1 0001 1011
100011011

write p left-aligned with result
and XOR

10011100111010
100011011
---------
   10001011010
   100011011
   -----------
        110110

= 0x36 = 54 decimal
```

That is the correct result.  We get the same answer from the log table:

```
log(b6) = 0xb1
log(53) = 0x30
            --
            e1
            
antilog(e1) = 0x36
```

Mindless ``(n % 256) ^ 27`` does not do the same thing.

```
    if r > 255:
        r = (r % 256) ^ 27
``` 

I wrote a function that mimics the graphical method:

```
def mod(n):
    p = 283 
    b = len(bin(p))
    while True:
        if n < 256:
            return n
        d = p << (len(bin(n)) - b)
        n = n ^ d
```

The two approaches give different results for ``n >= 512``.  Curiously it works again for 72192-72447 for ``n < 100000``.

#### Understanding dawns

The graphical method left-shifts ``100011011`` (283) until the first non-zero bit matches *n*.

*No shift is needed* for n < 512.  So in the range [256-511] first % 256 and then XOR 27 works.

The largest value generated in the powers of ``0x03`` is

```
  1010 1010
1 0101 010
-----------
1 1111 1110
```
So the shift is never necessary for making the powers of ``0x03`` table.  Note:  it would be necessary for the powers of ``0x07``, then for example

```
   1001 0011
10 0100 1100
-----------
10 1101 1111
```
and we *do* need a shift.

So what we could do is to count the number of places in *n*, subtract 9, left-shift 27 by that, and then do the XOR with n % 256.

However, this won't work for something like 

``11 1101 1111`` 

because two XOR's are needed.

I came up with this revised code:

```python
def mod(n):
    p = 283 
    b = len(bin(p))
    while True:
        if n < 256:
            return n
        d = p << (len(bin(n)) - b)
        n = n ^ d

def gmultiply(a,b):
    if a < b:
        a,b = b,a
    # the digits of binary b reversed
    s = bin(b)[2:][::-1]
    r = 0
    for c in s:
        if c == '1':
            r = r ^ a       # addition
        a = a << 1          # left-shift
    r = mod(r)
    return r
```

Left-shift 283 so that it lines up with the first bit in *n*.  Then do ``n = n ^ d``.  

Repeat until ``n < 256``.

The new function passes both tests in

```python
import gen_utils as ut

fn = 'g3.logs.ints.txt'
L = ut.load_data(fn)
D = dict()
for i,v in enumerate(L):
    D[i+1] = v
# print D[182], D[83], D[54]
# 177 48 225
# that's correct

for i in range(1,256):
    for j in range(1,256):
        p1 = ut.gmultiply(i,j)
        
        log = D[i] + D[j]
        for k in D:
            if D[k] == log:
                break
        p2 = k
        
        if p1 != p2:
            print i,j,i*j
        break

fn = 'mi.ints.txt'
with open(fn) as fh:
    data = fh.read()
for e in data.strip().split('\n'):
    t = e[1:-1].split(',')
    a,b = int(t[0]), int(t[1])
    # print("%d %d" % (a,b))
    
    p = ut.gmultiply(a,b)
    assert p == 1
    
```

The first checks if ``gen_utils.gmultiply`` gives the same result as obtained by using the table of logarithms, for all 65,000+ values in [1..255].

The second checks that when the function is used to multiply all the pairs in the table of multiplicative inverses, the result is always equal to 1.

#### Division

```
    while True:
        if n < 256:
            return n
        d = p << (len(bin(n)) - b)
        n = n ^ d
```

Recall that in the fields we're looking at, addition and subtraction are the same (XOR).

So, this is really the same as repeated subtraction of p, i.e. division.  At each step we multiply p by some multiple of 2, then add/subtract/XOR.


