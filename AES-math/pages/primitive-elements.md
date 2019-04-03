#### Primitive elements and generators

According to [wikipedia](https://en.wikipedia.org/wiki/Primitive_element_(finite_field)):

> a primitive element of a finite field GF(q) is a generator of the multiplicative group of the field. In other words, α ∈ GF(q) is called a primitive element if it is a primitive (q − 1)th root of unity in GF(q); this means that each non-zero element of GF(q) can be written as αi for some integer i.
> 

The first part means that for primitive element *g* and field *GF(n)* 

- <p> g<sup>n-1</sup> ``= 1 (mod n)``</p>

and

- ``g*i``for each ``i`` in [1..n] gives all of the elements of GF(n)

Recall that for n = 7, the primitive elements for the powers table are 3 and 5 and:

- 3<sup>n</sup> = 3
- 3<sup>n-1</sup> = 1

The same for 5.

#### GF(2e8)

The GF we are most interested in, of course, is GF(2<sup>8</sup>), with 256 elements.

It [turns out](http://www.cs.utsa.edu/~wagner/laws/FFM.html) that ``0x03`` is a generator of this field.

We can check this now.

As we saw, computations in the GF we'll define uses special rules:

- addition is XOR 
- multiplication is a left-shift plus a mod operation
- special modulus is 256 + 27 = 283

Multiplication by 3 is carried out as a left-shift plus addition to self (XOR with no carry). We obtain:

```
(011)**2 = 011 * 011 = 110 + 011 =   0000 0101 = 05
(011)**3 = 0000 1010 + 0000 0101 =   0000 1111 = 0f
(011)**3 = 0001 1110 + 0000 1111 =   0001 0001 = 11
(011)**4 = 0010 0010 + 0001 0001 =   0011 0011 = 33
(011)**5 = 0110 0110 + 0011 0011 =   0101 0101 = 55
(011)**6 = 0101 0101 + 0101 0101 =   1111 1111 = ff
(011)**7 = 1111 1110 + 1111 1111 = 1 0000 0001 = ?
```
The value has exceeded 256, so the modulus operation is invoked.  We cannot explain why 283 is special at the moment.  We XOR the result with:

- ``1 0001 1011`` (the last 8 digits equal decimal 27).

```
1 0001 1011
1 0000 0001
---------
0 0001 1010 = 26 = 1a
```

I wrote a Python function to do this multiplication

```python
def gmultiply(a,b,p=283):
    # for efficiency
    if a < b:
        a,b = b,a
        
    # the digits of binary b (reversed)
    s = bin(b)[2:][::-1]
    
    r = 0
    # for each digit in b (reversed)
    # add a to accumulated result
    # where a is left-shifted 
    # by digit's place in b (reversed)
    for c in s:
        if c == '1':
            r = r ^ a       # addition
        a = a << 1          # left-shift
    return gmod(r,p)
```

- addition is XOR
- multiplication is left-shift by binary digits of multiplicand followed by XOR
- modulus is 283 = 256 + 27

and another to to the modulus operation:

```
def gmod(n,p):  # 283 is standard
    # leave leading '0b'
    b = len(bin(p))
    
    # repeatedly
    while True:
        if n < 256:
            return n
        # shift p out to match n
        d = p << (len(bin(n)) - b)
        n = n ^ d
```

**Note**:  the first version of this function is not quite correct.  

It correctly generated the powers of ``0x03`` and so we get the correct table of exponents, and later logarithms.  

But it did not give the correct answer for:

```
0xb6 * 0x53 = 0x36
182  * 83   = 54
```

The current version is correct.

We'll see reason the reason for that in a bit.

**output** for g = 3

```
01 03 05 0f 11 33 55 ff 1a 2e 72 96 a1 f8 13 35
5f e1 38 48 d8 73 95 a4 f7 02 06 0a 1e 22 66 aa
e5 34 5c e4 37 59 eb 26 6a be d9 70 90 ab e6 31
53 f5 04 0c 14 3c 44 cc 4f d1 68 b8 d3 6e b2 cd
4c d4 67 a9 e0 3b 4d d7 62 a6 f1 08 18 28 78 88
83 9e b9 d0 6b bd dc 7f 81 98 b3 ce 49 db 76 9a
b5 c4 57 f9 10 30 50 f0 0b 1d 27 69 bb d6 61 a3
fe 19 2b 7d 87 92 ad ec 2f 71 93 ae e9 20 60 a0
fb 16 3a 4e d2 6d b7 c2 5d e7 32 56 fa 15 3f 41
c3 5e e2 3d 47 c9 40 c0 5b ed 2c 74 9c bf da 75
9f ba d5 64 ac ef 2a 7e 82 9d bc df 7a 8e 89 80
9b b6 c1 58 e8 23 65 af ea 25 6f b1 c8 43 c5 54
fc 1f 21 63 a5 f4 07 09 1b 2d 77 99 b0 cb 46 ca
45 cf 4a de 79 8b 86 91 a8 e3 3e 42 c6 51 f3 0e
12 36 5a ee 29 7b 8d 8c 8f 8a 85 94 a7 f2 0d 17
39 4b dd 7c 84 97 a2 fd 1c 24 6c b4 c7 52 f6 01
```

This matches my [source](http://www.cs.utsa.edu/~wagner/laws/FFM.html).  There are other "primitive elements."  

**output** for g = 6

```
01 06 14 78 0b 3a 9c 65 45 85 33 aa d1 d0 d6 c2
ba b1 8b 17 72 37 b2 81 2b fa 2a fc 3e 84 35 be
a9 db ec 5e df f4 0e 24 d8 e6 62 57 e9 40 9b 77
29 f6 02 0c 28 f0 16 74 23 ca 8a 11 66 4f b9 bb
b7 9f 6f 79 0d 2e e4 6e 7f 19 56 ef 54 e3 7c 13
6a 67 49 ad c3 bc a5 f3 1c 48 ab d7 c4 ae c9 80
2d ee 52 f7 04 18 50 fb 2c e8 46 8f 0f 22 cc 9e
69 6d 75 25 de f2 1a 5c d3 dc fe 32 ac c5 a8 dd
f8 26 d4 ce 92 41 9d 63 51 fd 38 90 4d b5 93 47
89 1b 5a c7 a4 f5 08 30 a0 ed 58 cb 8c 05 1e 44
83 27 d2 da ea 4a a7 ff 34 b8 bd a3 e7 64 43 91
4b a1 eb 4c b3 87 3f 82 21 c6 a2 e1 70 3b 9a 71
3d 8e 09 36 b4 95 53 f1 10 60 5b c1 b0 8d 03 0a
3c 88 1d 4e bf af cf 94 55 e5 68 6b 61 5d d5 c8
86 39 96 59 cd 98 7d 15 7e 1f 42 97 5f d9 e0 76
2f e2 7a 07 12 6c 73 31 a6 f9 20 c0 b6 99 7b 01
```

These are tables of the **powers** of the base, either ``0x03``  or ``0x06`` in GF(2<sup>8</sup>).

We could call it a table of **exponents**.  We'll use it going forward.  