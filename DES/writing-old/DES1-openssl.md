### Doing ECB using openssl

#### Summary

* Input the key as hex on the command line with ``-K``.

* Use ``-nopad``

```
> openssl des-ecb -e -nopad -K "0E329232EA6D0D73" -in m87.bin | xxd -p
0000000000000000
>
```

#### Preliminary

The CryptoPals challenge suggests

> You can obviously decrypt this using the OpenSSL command-line tool, but we're having you get ECB working in code for a reason. 

They want me to **actually do encryption according to DES** and maybe later, AES, in code.  

It took me a while to find a reference that doesn't just do ECB at the command line or in Python with ``pycrypto`` or whatever...  

Wikipedia has a long [article](https://en.wikipedia.org/wiki/Data_Encryption_Standard) but it's helpful to have an example to check your code against.

I finally found a [reference](http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm) on the web.  

How cool is that?

Now that I've done it, it wasn't a huge challenge except there are a lot of steps so it took me basically a whole day.  

On this page, we will just set the stage.  Implementing CBC and ECB will be for another page.  Begin at the beginning.

### DES overview

We will just try out the **openssl** version (sorry, CryptoPals).

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

Although this result looks magical, don't forget that the same key operating on 

```
0000000000000000
```

in decrypt mode will give 

```
8787878787878787
```

### Operational Details

From examples I've seen on the web I know that the first part of the command is 

```
openssl des-ecb -e
```

Encrypt is the default but we will provide the ``-e`` flag anyway.  Next is the key.

From reading the man page (``man openssl``), the key parameter is a binary string of 8 bytes.  On that page there is no mention of an input file.  There is also no discussion of the difference between ``-k`` and ``-K`` (but see below).

The man pages are famously hard to parse.  I finally found [this](https://wiki.openssl.org/index.php/Command_Line_Utilities#Basic_file) which gives me

```
openssl enc --help
unknown option '--help'
options are
-in <file>     input file
-out <file>    output file
-pass <arg>    pass phrase source
-e             encrypt
-d             decrypt
-a/-base64     base64 encode/decode, depending on encryption flag
-k             passphrase is the next argument
-kfile         passphrase is the first line of the file argument
-md            the next argument is the md to use to create a key
                 from a passphrase.  One of md2, md5, sha or sha1
-S             salt in hex is the next argument
-K/-iv         key/iv in hex is the next argument
-[pP]          print the iv/key (then exit if -P)
-bufsize <n>   buffer size
-nopad         disable standard block padding
-engine e      use engine e, possibly a hardware device.
```

What I get from this is that the ``-k`` flag is followed by a passphrase, while ``-K`` is followed by the hex-encoded key.  No files with these.  However, we have ``-kfile`` which says that the "passphrase is the first line of the file."

We were given ``0E329232EA6D0D73`` as the key.

Our first step is to get the plaintext on disk:

```bash
> printf "\x87\x87\x87\x87\x87\x87\x87\x87" > m87.bin
> hexdump m87.bin
0000000 87 87 87 87 87 87 87 87                        
0000008
>
```

#### Encrypt

Make sure to use DES and ECB.  Following the manual, we use ``-K`` followed by our hex key.

Piping the output to ``xxd`` "creates a hex dump of a given file or standard input."  The ``-p`` flag means "plain" (no byte counts or ASCII equivalents).

```bash
> openssl des-ecb -e -K "0E329232EA6D0D73" -in m87.bin | xxd -p
0000000000000000a913f4cb0bd30f97
> openssl des-ecb -e -K "0E329232EA6D0D73" -in m87.bin -out enc.bin
> hexdump enc.bin 
0000000 00 00 00 00 00 00 00 00 a9 13 f4 cb 0b d3 0f 97
0000010
>
```

That's half-right.  If we try reversing the encryption:

```bash
> openssl des-ecb -d -K "0E329232EA6D0D73" -in enc.bin | xxd -p
8787878787878787
> openssl des-ecb -d -K "0E329232EA6D0D73" -in enc.bin -out tmp.bin
> hexdump tmp.bin
0000000 87 87 87 87 87 87 87 87                        
0000008
>
```

We get the correct plaintext back without anything extra.

So that kinda sorta works.  

What seems to be happening is that an 8 byte block of padding is being added for encryption, and it's not displayed on decryption.  The question is:  why would you pad a full block?

I found the answer on StackOverflow [here](http://crypto.stackexchange.com/questions/12621/why-does-openssl-append-extra-bytes-when-encrypting-with-aes-128-ecb) with this quote

> padding is always applied. So, in the case of a full input block, another full block of ``0x10`` bytes will be added as padding, which means you'll have two blocks of output (which is what you see above).

As you can see in the man page above there is a ``-nopad`` flag:

> The -nopad option for openssl enc disables padding (but it will throw an error if your input isn't a multiple of the block size):


So even though our plaintext was exactly 8 bytes, openssl added an extra block of 8 bytes to the input.


```bash
> openssl des-ecb -e -nopad -K "0E329232EA6D0D73" -in m87.bin | xxd -p
0000000000000000
>
```

A small contradiction to the StackOverflow answer above, from what I read before (about **PKSC#7**) [here](https://en.wikipedia.org/wiki/Padding_cryptography), the pad should be constructed from the byte whose value is the number of bytes needed: '\x08' * 8.  

Try it.

```bash
> printf "\x87\x87\x87\x87\x87\x87\x87\x87\x08\x08\x08\x08\x08\x08\x08\x08" > m87p.bin
> openssl des-ecb -e -nopad -K "0E329232EA6D0D73" -in m87p.bin | xxd -p
0000000000000000a913f4cb0bd30f97
>
```

When we do ``-nopad`` but manually add our own padding according to **PKCS7**, the extra bytes we get match the bytes we got above: ``a913f4cb0bd30f97``. 

It looks good.  We conclude that openssl just padded our input with ``\x08`` * 8.

And it's not just that openssl thinks the message should be at least 16 bytes, if we add our pad and then do

```bash
> printf "\x87\x87\x87\x87\x87\x87\x87\x87\x08\x08\x08\x08\x08\x08\x08\x08" > out.bin
> openssl des-ecb -e -K "0E329232EA6D0D73" -in out.bin -out enc.bin
> hexdump enc.bin
0000000 00 00 00 00 00 00 00 00 a9 13 f4 cb 0b d3 0f 97
0000010 a9 13 f4 cb 0b d3 0f 97                        
0000018
>
```

It pads out to 24 with another 8 bytes.

#### Key from a passphrase, or from a file.

TL;DR  doesn't work

Case makes a difference:

```
> openssl des-ecb -e -nopad -k "0E329232EA6D0D73" -in m87.bin | xxd -p
53616c7465645f5f529efeda5012da1d8f9638d4839cbe69
>
```

``-k`` is supposed to be a passphrase, but I don't know what that would be.  The ASCII for ``0E329232EA6D0D73`` is not English.  What about a key file?

Suppose we put the hex as ASCII into a file?

```bash
> echo -n "0E329232EA6D0D73" > key.txt
> hexdump -C key.txt
00000000  30 45 33 32 39 32 33 32  45 41 36 44 30 44 37 33  |0E329232EA6D0D73|
00000010
>
```

```bash
> openssl des-ecb -e -nopad -kfile key.txt -in m87.bin | xxd -p
53616c7465645f5f25c9a4bf36baa212ecb39abbd6a9a29d
>
```

Nope.  What about binary data:

```bash
> printf "\x0e\x32\x92\x32\xea\x6d\x0d\x73" > key.bin
> hexdump key.bin
0000000 0e 32 92 32 ea 6d 0d 73                        
0000008
>
```

```bash
> openssl des-ecb -e -nopad -kfile key.bin -in m87.bin | xxd -p
53616c7465645f5ff3e30ce0bfe19d7a2c1166f4f7dd5066
>
```

Hmm.  Maybe it should be ASCII:

```
> openssl des-ecb -e -nopad -kfile key.txt -in m87.bin | xxd -p
53616c7465645f5ff79504de99d74c7fdf7733fcfe6a4e45
>
```

That's weird, neither the binary nor the text form of the key works.  And we get the same wrong answer with each.  We get the identical result with ``-k`` instead of ``-kfile``.

```
> openssl des-ecb -e -nopad -k key.bin -in m87.bin | xxd -p
53616c7465645f5fbe424d3a7c49ba862ecfdc20ac97d9a9
> openssl des-ecb -e -nopad -k key.txt -in m87.bin | xxd -p
53616c7465645f5f98bde21509f3d2e8c042c7d437d79695
>
```

So... openssl gets the same key from binary data or hex-encoded data, and ``-k`` works the same as ``-kfile``, but neither gives the correct result, which we obtain with ``-K`` and the hex provided on the command line.

#### Example from the DES ECB tutorial.

There is another example in the [reference](http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm).  The message is

> "Your lips are smoother than vaseline"

I use Python to get the message on disk.

```bash
>>> s = "Your lips are smoother than vaseline"
>>> L = [ord(c) for c in s]
>>> ba = bytearray(L)
>>> import utils as ut
>>> ut.writeData('out.bin', ba, mode = 'wb')
>>> 
```

```bash
> hexdump out.bin
0000000 59 6f 75 72 20 6c 69 70 73 20 61 72 65 20 73 6d
0000010 6f 6f 74 68 65 72 20 74 68 61 6e 20 76 61 73 65
0000020 6c 69 6e 65                                    
00
```

That looks fine, except that what we were really supposed to do is to add the newline from Windows ``0d0a`` and also two more zero bytes ``0000``

```python
>>> s = "Your lips are smoother than vaseline"
>>> L = [ord(c) for c in s]
>>> L.extend([13, 10, 0, 0])
>>> ba = bytearray(L)
>>> import utils as ut
>>> ut.writeData('out.bin', ba, mode = 'wb')
>>>
```

```bash
> hexdump out.bin
0000000 59 6f 75 72 20 6c 69 70 73 20 61 72 65 20 73 6d
0000010 6f 6f 74 68 65 72 20 74 68 61 6e 20 76 61 73 65
0000020 6c 69 6e 65 0d 0a 00 00                        
0000028
>
```

We encrypt it as before:

```bash
> openssl des-ecb -nopad -e -K "0E329232EA6D0D73" -in out.bin -out enc.bin
> hexdump enc.bin
0000000 c0 99 9f dd e3 78 d7 ed 72 7d a0 0b ca 5a 84 ee
0000010 47 f2 69 a4 d6 43 81 90 d9 d5 2f 78 f5 35 84 99
0000020 82 8a c9 b4 53 e0 e6 53                        
0000028
> 
```

This matches what they have in the article.

<hr>

#### Key size

```bash
> openssl des-ecb -e -nopad -K "YELLOW SUBMARINE" -in m87.bin | xxd -p
non-hex digit
invalid hex key value
> openssl des-ecb -e -nopad -K "0E329232EA6D0D73" -in m87.bin | xxd -p
0000000000000000
> openssl des-ecb -e -nopad -K "0E329232EA6D0D730E329232EA6D0D73" -in m87.bin | xxd -p
0000000000000000
> openssl des-ecb -e -nopad -K "0E329232EA6D0D73FFFFFFFFFFFFFFFF" -in m87.bin | xxd -p
0000000000000000
>
```
