#### Key expansion

The 128-bit key is expanded to give 10 4-byte round keys plus an initial 4-bytes.  These 4-bytes are XOR'd with the input block before the rounds start.

The round keys are used in reverse order for decryption.

These two figures show a bit about the expansion:

![](figs/aes1.png) 

First of all, if we write the key in a matrix format, the 128-bit key forms four 32-bit (4-byte) words as shown.

This next figure shows the basic idea for expansion:

![](figs/aes2.png)

We take the whole key ``w0 w1 w2 w3`` and generate ``g``.  Then 

* w4 =  g &#8853; w0
* w5 = w4 &#8853; w1
* w6 = w5 &#8853; w2
* w7 = w6 &#8853; w3

* w8 = g &#8853; w4
* w9 = w8 &#8853; w5

and so on.

#### Getting to g

g is generated from the last word of the previous round.  The first value comes from g(w3).

Page 39.  The function g consists of 3 steps:

* perform a one-byte left circular rotation on the entire word
* for each byte of the word, perform byte substitution using the S-box as in SubBytes above.
* XOR the resulting bytes with a **round constant**

> The round constant is a word whose three rightmost bytes are always zero.

So now all we need is the non-zero leftmost byte.

* ``RC[0] = \x01``
* ``RC[i] = \x02 x RC[i-1]``

This is GF multiplication where the rule is to do a non-wrapping left-shift and then if the value is >= 127, do an XOR with 27.

It sounds complicated but we can generate the results as a table:

```python
L = [1]
for i in range(14):
    n = L[-1]
    m = (n << 1) % 256
    if n > 127:
        m = m ^ 27
    L.append(m)

print L
```
prints:

```
[1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47]
>>> 
```

Or as given [here](http://www.adamberent.com/documents/AESbyExample.pdf) (on page 12), in hex:

```
01 02 04 08 10 20 40 80 1b 36 6c d8 ab 4d 9a 
```

Justs check it:

```python
>>> s = '01 02 04 08 10 20 40 80 '
>>> s += '1b 36 6c d8 ab 4d 9a'
>>> [int(h,16) for h in s.split()]
[1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154]
>>>
```

Kak gives an example in his chapter 8.  

The key is "hello", padded to 16 with '0' or 48 as an int.

```
word 0: [104, 101, 108, 108]
word 1: [111, 48, 48, 48]
word 2: [48, 48, 48, 48]
word 3: [48, 48, 48, 48]
word 4: [109, 97, 104, 104]
word 5: [2, 81, 88, 88]
word 6: [50, 97, 104, 104]
word 7: [81, 88, 88, 2]
word 8: [190, 11, 2, 31]
word 9: [188, 90, 90, 71]
word 10: [142, 59, 50, 47]
word 11: [99, 106, 45, 223]..```
with round keys

```
68656c6c6f3030303030303030303030
6d616868025158583261686851585802
be0b021fbc5a5a478e3b322f636a2ddf 
..
```

So the next step is to try to code the key expansion in Python.

#### Python implementation of expand

That code is in the same folder as this file in **aes_key.py** (example 1).  Up to round 2 I got

```python
> python aes_key.py 
 0 68 65 6c 6c [104, 101, 108, 108]
 1 6f 30 30 30 [111, 48, 48, 48]
 2 30 30 30 30 [48, 48, 48, 48]
 3 30 30 30 30 [48, 48, 48, 48]

 4 6d 61 68 68 [109, 97, 104, 104]
 5 02 51 58 58 [2, 81, 88, 88]
 6 32 61 68 68 [50, 97, 104, 104]
 7 02 51 58 58 [2, 81, 88, 88]

 8 be 0b 02 1f [190, 11, 2, 31]
 9 bc 5a 5a 47 [188, 90, 90, 71]
10 8e 3b 32 2f [142, 59, 50, 47]
11 8c 6a 6a 77 [140, 106, 106, 119]
>
```

Compare to his output:

![](figs/Kak4.png) 

We diverge at word 7.  I believe this is an error in the source.  One reason for thinking this is that w7 is formed very simply, from w3 XOR w6.

![](figs/aes2.png)

But w3[0] is 48 and w6[0] is 50 and the result should then be 48 ^ 50 = 2, which matches what I have.  

Also, his output is a shifted version of mine.

#### Another source

More than this, I have another [source](http://www.cse.wustl.edu/~jain/cse571-11/ftp/l_05aes.pdf).

On slide 11 he lists 

![](figs/Jain1.png)  

Now, there is an error here, namely, he has dropped one byte from w2.  Still, we can recover it, since 

w6 = w5 &#8853; w2

Hence

w2 = w5 &#8853; w6

It is easily shown that the first three bytes are correct and the fourth one should be

e9 &#8853; 3f = d6

```
>>> int('e9',16) ^ int('3f',16)
214
>>> hex(214)
'0xd6'
>>>
```

I convert his hex digits for w0-w4 into ints and have

```
[[15,21,113,201],
 [71,217,232,89],
 [12,183,173,214],
 [175,127,103,152]]
```
A run of my expansion code in **aes_key.py** (example 3) for two rounds generates:

```
> python aes_key.py 
 0 0f 15 71 c9 [15, 21, 113, 201]
 1 47 d9 e8 59 [71, 217, 232, 89]
 2 0c b7 ad d6 [12, 183, 173, 214]
 3 af 7f 67 98 [175, 127, 103, 152]

 4 dc 90 37 b0 [220, 144, 55, 176]
 5 9b 49 df e9 [155, 73, 223, 233]
 6 97 fe 72 3f [151, 254, 114, 63]
 7 38 81 15 a7 [56, 129, 21, 167]

 8 d2 c9 6b b7 [210, 201, 107, 183]
 9 49 80 b4 5e [73, 128, 180, 94]
10 de 7e c6 61 [222, 126, 198, 97]
11 e6 ff d3 c6 [230, 255, 211, 198]

>
```

which matches our new source exactly.  Unfortunately for me, he does not list his entire output.

I would like to have a source that does that before I try to do the rest of the code.

I found another one [here](https://kavaliro.com/wp-content/uploads/2014/03/AES.pdf)

Back to **aes_key.py** (example 4).  I have

```
> python aes_key.py 
 0 54 68 61 74 [84, 104, 97, 116]
 1 73 20 6d 79 [115, 32, 109, 121]
 2 20 4b 75 6e [32, 75, 117, 110]
 3 67 20 46 75 [103, 32, 70, 117]

 4 e2 32 fc f1 [226, 50, 252, 241]
 5 91 12 91 88 [145, 18, 145, 136]
 6 b1 59 e4 e6 [177, 89, 228, 230]
 7 d6 79 a2 93 [214, 121, 162, 147]

 8 56 08 20 07 [86, 8, 32, 7]
 9 c7 1a b1 8f [199, 26, 177, 143]
10 76 43 55 69 [118, 67, 85, 105]
11 a0 3a f7 fa [160, 58, 247, 250]

12 d2 60 0d e7 [210, 96, 13, 231]
13 15 7a bc 68 [21, 122, 188, 104]
14 63 39 e9 01 [99, 57, 233, 1]
15 c3 03 1e fb [195, 3, 30, 251]

16 a1 12 02 c9 [161, 18, 2, 201]
17 b4 68 be a1 [180, 104, 190, 161]
18 d7 51 57 a0 [215, 81, 87, 160]
19 14 52 49 5b [20, 82, 73, 91]

20 b1 29 3b 33 [177, 41, 59, 51]
21 05 41 85 92 [5, 65, 133, 146]
22 d2 10 d2 32 [210, 16, 210, 50]
23 c6 42 9b 69 [198, 66, 155, 105]

24 bd 3d c2 87 [189, 61, 194, 135]
25 b8 7c 47 15 [184, 124, 71, 21]
26 6a 6c 95 27 [106, 108, 149, 39]
27 ac 2e 0e 4e [172, 46, 14, 78]

28 cc 96 ed 16 [204, 150, 237, 22]
29 74 ea aa 03 [116, 234, 170, 3]
30 1e 86 3f 24 [30, 134, 63, 36]
31 b2 a8 31 6a [178, 168, 49, 106]

32 8e 51 ef 21 [142, 81, 239, 33]
33 fa bb 45 22 [250, 187, 69, 34]
34 e4 3d 7a 06 [228, 61, 122, 6]
35 56 95 4b 6c [86, 149, 75, 108]

36 bf e2 bf 90 [191, 226, 191, 144]
37 45 59 fa b2 [69, 89, 250, 178]
38 a1 64 80 b4 [161, 100, 128, 180]
39 f7 f1 cb d8 [247, 241, 203, 216]

40 28 fd de f8 [40, 253, 222, 248]
41 6d a4 24 4a [109, 164, 36, 74]
42 cc c0 a4 fe [204, 192, 164, 254]
43 3b 31 6f 26 [59, 49, 111, 38]
> 
```

You don't have to check the whole thing.  He has

```
Round 10: 28 FD DE F8 6D A4 24 4A CC C0 A4 FE 3B 31 6F 26
```

That's a match!  Anybody else?

[This one](http://www.samiam.org/key-schedule.html) gives examples of the entire output for 4 input keys:

```
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f
69 20 e2 99 a5 20 2a 6d 65 6e 63 68 69 74 6f 2a
```

He also gives examples for larger (192 and 256-bit) keys.

Here is my output for his examples.  Rather than print the whole thing, I just put the first four and the last four words.

```bash
> python aes_key.py 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
b4 ef 5b cb 3e 92 e2 11 23 e9 51 cf 6f 8f 18 8e

ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
d6 0a 35 88 e4 72 f0 7b 82 d2 d7 85 8c d7 c3 26

00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f
13 11 1d 7f e3 94 4a 17 f3 07 a7 8b 4d 2b 30 c5

69 20 e2 99 a5 20 2a 6d 65 6e 63 68 69 74 6f 2a
ae 12 7c da db 47 9b a8 f2 20 df 3d 48 58 f6 b1

>
```

Compare with his output:

```
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
b4 ef 5b cb 3e 92 e2 11 23 e9 51 cf 6f 8f 18 8e

ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff 
d6 0a 35 88 e4 72 f0 7b 82 d2 d7 85 8c d7 c3 26

00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f
13 11 1d 7f e3 94 4a 17 f3 07 a7 8b 4d 2b 30 c5

69 20 e2 99 a5 20 2a 6d 65 6e 63 68 69 74 6f 2a
ae 12 7c da db 47 9b a8 f2 20 df 3d 48 58 f6 b1
```

I believe that's a match.