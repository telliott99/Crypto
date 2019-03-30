TL;DR

Using ``openssl``

- Input the key as hex on the command line with ``-K``
- Use ``-nopad``

```
> openssl des-ecb -e -nopad \
-K "0E329232EA6D0D73" -in m87.bin | \
xxd -p
0000000000000000
>
```

#### openssl

DES encryption uses 64-bit keys, 8 byte keys.  

The effective key size is 56 bits, but that's another story.  

In the first part of the tutorial from the link above, we are given the plaintext message as

```
8787878787878787
```

and told that it is 8 bytes.  Our conclusion is that this must be hex.  The key is given as 

```
0E329232EA6D0D73
```

which seems obviously to be hex as well, and it is claimed that encryption by DES will give 

```
0000000000000000
```

Our plaintext message is ``8787878787878787``.  I believe this must be bytes.  We [write](write-bytes.md) 8 bytes to disk.  

**command**:

```
openssl des-ecb -e -nopad \
-K "0E329232EA6D0D73" -in m87.bin | \
xxd -p
```

**output**:

```
0000000000000000
>
```

As the source says.  

The ``xxd -p`` part says to take the output bytes and run hexdump in ``-p`` plain style (i.e. continuous).

``m87.bin`` is in the files directory, but there's no point in linking to it.

#### decrypt

**command**:

```
echo -ne '\x00\x00\x00\x00' > m0.bin
echo -ne '\x00\x00\x00\x00'  >> m0.bin
hexdump -C m0.bin
```

**output**:

```
00000000  87 87 87 87 87 87 87 87                           |........|
00000008
>
```

**command**:

```
openssl des-ecb -d -nopad \
-K "0E329232EA6D0D73" -in m0.bin | \
xxd -p
```

Notice ``-d``.

**output**:

```
8787878787878787
```

You might wonder how the guy figured out this was the right key.

