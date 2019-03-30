#### operations

- addition is not standard addition, it is XOR
- multiplication is not standard multiplication
- values are produced mod 283, with a special rule

Here are three examples.

```
    0000 0101  0x05 =  5
    0000 0011  0x03 =  3
    ---------
    0000 0101
    0000 1010
    ---------
    0000 1111  0x0f = 15
```

- ``0x03 x 0x05 = 0x15``.  That looks normal enough.

```
    0000 1111  0x0f = 15
    0000 0011  0x03 =  3
    ---------
    0000 1111
    0001 1110
    ---------
    0001 0001  0x11 = 17
```

- ``0x03 x 0x0f = 0x11``:  we see the effect of XOR.


```
    1111 1111  0xff
    0000 0011  0x03
    ---------
    1111 1111
  1 1111 1110
  -----------
  1 0000 0001
% 1 0001 1011  0x011b = 283
  -----------
    0001 1010  0x1a
```

- we see the effect of the mod rule plus XOR.

The unusual aspect is that if the result of multiplication *n* is 

- 255 < n < 283

as it is above, one **still does XOR**.

The math of Galois fields explains how this all comes about.