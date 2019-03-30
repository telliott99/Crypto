### Implementation of DES-ECB in Python

I just wanted to see if I could do it.

This project contains the Python code that I wrote to implement DES in ECB mode.  Here we will just quickly skim the highlights of the various steps.  

If you're interested in this you should work through the tutorial (a copy is in this directory) and the original is [here](http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm).

Having said that, you could always take copy my nicely laid out and proofed S boxes and permutation matrices and such from [here](../DES-code/pydes/info.py).

#### Format for the data

Inputs and outputs are 8-byte keys and blocks.  

It's an unusual choice (normally for cryptography I would use lists of bytes as ints), but I decided to work with strings and lists of binary digits as '0' and '1'.  It made it easy to check my results against the tutorial.

So if you examine a key list (usually ``kL``), you will see ``['0', '1' .. ]``.  

For display, we call ``pchunks(L, SZ=8, ONELINE=4)`` which generates ``['01011101 11111111 .. ' ]`` or something like it.  

In various places we might want 4, 6, 7 or 8 bits in each chunk.

We take the key and message (``msg``) as hex-encoded strings and first convert them to this format:

```
key = ut.convertHexKeyInput(key)
msg = ut.convertHexKeyInput(msg)
```

gives a formatted string, and

```
kL = ut.filter_01(key)
```

gives a list of ``0`` and ``1``.

#### 1a. First permutation

```
PC1 = '''
57  49  41  33  25  17   9   0
 1  58  50  42  34  26  18   0
10   2  59  51  43  35  27   0
19  11   3  60  52  44  36   0
63  55  47  39  31  23  15   0
 7  62  54  46  38  30  22   0
14   6  61  53  45  37  29   0
21  13   5  28  20  12   4   0
'''
```

In the first step, we re-order the bits of the key, according to this schedule.  The 57th bit of the key becomes the first bit of the output, and so on.  Every 8th bit is discarded.  The indexing is 0-based.  There are several such operations all together.

The input is a 64-bit key, and the output is only 56 bits.  For such keys, we display the bits in blocks of 7.

#### 1b. Shifting

The second step is to "shift" the key to form a set of 16 keys called a "key schedule".  The shift is a left-shift that wraps.  

Each key is divided into a left and right half and the two halves are shifted independently.  They are then combined again after each shift to form the output.

The left-half of the key generated in step 1a is:

```
1111000 0110011 0010101 0101111
```

The left halves of the first three keys generated in step 1b are:

```
1110000 1100110 0101010 1011111
1100001 1001100 1010101 0111111
0000110 0110010 1010101 1111111
0011001 1001010 1010111 1111100
```

what's going on is that the shifts are in this order:

```
[1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
```

so for the first two we have left-shifted by 1, and for the third, we left-shifted by 2.

```
1110000 1100110 0101010 1011111
1100001 1001100 1010101 0111111
0000110 0110010 1010101 1111111
0011001 1001010 1010111 1111100
```

The right side of each picked up the values shifted off the left side.

#### 1c.  Second permutation

Each of the 16 keys generated in 1b is permuted according to the schedule PC2.

```
PC2 = '''
14  17  11  24   1   5   0
 3  28  15   6  21  10   0
23  19  12   4  26   8   0
16   7  27  20  13   2   0
41  52  31  37  47  55   0
30  40  51  45  33  48   0 
44  49  39  56  34  53   0
46  42  50  36  29  32   0
'''
```

In PC2, every 7th bit is discarded.  The result is 16 keys that each look like this (showing the left and right halves on successive lines):

```
000110 110000 001011 101111
111111 000111 000001 110010
```

Each key is now 48-bits.

#### 1d.  Message permutation

At this point, we shift our attention to the message.  It is permuted according to ``IP``.  No bits are discarded, naturally.  The key is still 64-bits.

(This step was originally numbered 2a in the "old" code).

We have five steps to go, four of them repeated 16 times each.  These are collectively referred to as the "f" function.  The last step is just carried out once.

### 2.  Overview

We will do multiple rounds of the steps that follow.  The first input is the permuted message block generated in 1d (64 bits).  The second input is the list of 16 keys of 48 bits each from 1c.

```
result = do_multiple_rounds_2b(mL, kLL)
```

This ``kLL`` is a list of key lists.

Inside the function ``do_multiple_rounds_2b`` we break the message into left and right halves:  ``Ln`` and ``Rn``.

On step 1 these could be called ``L0`` and ``R0``.

We use ``L`` and ``R`` and the i-th key from the key list, and generate a new version of ``R``.  The previous version ``R`` becomes the new ``L``.

```python
    L = mL[:32]
    R = mL[32:]
    
    for i in range(16):
        # get the ith key
        kL = ut.filter_01(input[i])
        nextR = one_round_2b(L, R, kL)
        L = R
        R = nextR
```

#### 2a.  Expansion

The first step of each individual round is to expand the 32-bit ``R`` to 48 bits.  In round 1 this ``R`` is just the right-half of the message, but later ``R``'s have been generated in previous rounds.

Some bits must be re-used (obviously) in this process.  The schedule is E_TABLE.

```
E_TABLE = '''
32   1   2   3   4   5
 4   5   6   7   8   9
 8   9  10  11  12  13
12  13  14  15  16  17
16  17  18  19  20  21
20  21  22  23  24  25
24  25  26  27  28  29
28  29  30  31  32   1
'''
```

#### 2b.  XOR with the key

This step is to XOR the 48-bit expanded ``R`` with the key for this round.

#### 2c.  Use the S-boxes

There are 8 S-boxes, the first one looks like this:

```
S1 = '''
14  4 13  1  2 15 11  8  3 10  6 12  5  9  0  7
 0 15  7  4 14  2 13  1 10  6 12 11  9  5  3  8
 4  1 14  8 13  6  2 11 15 12  9  7  3 10  5  0
15 12  8  2  4  9  1  7  5 11  3 14 10  0  6 13
'''
```

For each 48-bit block, we break it into 8 6-bit chunks.  The first chunk uses the first S-box, the second chunk the second S-box, and so on.

Each chunk of 6 bits is decoded to give a row and column (an address) in the S-box.  For example, from ``011011`` we take the first and last bit as ``01`` which is row 1 (0-based indexing).  We will find our output in the row that starts 

```
[0, 15, 7 ..]
```

The inner four bits are ``1101`` or 13 (0-based indexing, again).  The last index in each row is column 15.  Hence our value is decimal 5.

We convert 5 to ``0101`` and output that for this position in the key.  The result is 32-bits for each block.

#### 2d.  Permute according to schedule P.

```
P = '''
16   7  20  21
29  12  28  17
 1  15  23  26
 5  18  31  10
 2   8  24  14
32  27   3   9
19  13  30   6
22  11   4  25
'''
```

The output is 32 bits.

#### 2e.  XOR with the L input.

After this XOR step we return 32 bits to the caller.

### Final stages

So after 16 rounds of the second phase, we now have an ``L`` and ``R`` we could call ``L16`` and ``R16``.  These are combined in reverse order:  ``R16L16``.  The result is 64 bits.

In the final, final step we carry out one more permutation with:

```
IP_inv = '''
40   8  48  16  56  24  64  32
39   7  47  15  55  23  63  31
38   6  46  14  54  22  62  30
37   5  45  13  53  21  61  29
36   4  44  12  52  20  60  28
35   3  43  11  51  19  59  27
34   2  42  10  50  18  58  26
33   1  41   9  49  17  57  25
'''
```

And that's it!

#### Decrypting

One last thing, to decrypt, all that is necessary is to use the keys in ``kLL`` in reverse order.

```python
    # this is all it takes
    if mode == 'decrypt': 
        kLL.reverse()
```

#### Usage

I put it all in a package:  ``pydes``.  Use it like this:

```python
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

