### SHA digests

#### Gentle start

This project consists of scripts that implement SHA-1, SHA-256, and SHA-512 in Python.

A preliminary section deals with the derivation of some "magic" constants used in the various digest algorithms.  The details are [here](sha-magic.md), but basically these are constants that introduce randomness into the process, while it is completely transparent where the constants come from.

I started (after some false trails) with SHA-1 as the easiest to implement.  The first working version is [here](sha1.orig.py), and the description is [here](sha-md).

That program carries out SHA-1 on the simple message "abc" as outlined in the first example of the official documentation.

Various wrappers of Python bitwise functions are in [bits.py](bits.py), while SHA-specific constants and functions are in [funcs.py](funcs.py), (X = 1, 256 or 512), while the higher-level code is in [sha1.py](sha1.py). 

To begin with, the message text was hard-coded into the script, and it consists of just 3 bytes.

After padding to a multiple of the block size, the length of the message appears at the end of the message, but early on we do not construct the padding ourselves.  Instead, the whole thing is just given as a string.

In this first version, there is only a single block.  After a lot of hard work, we do match the output from `openssl`

```
> printf "abc" > x.txt
> openssl dgst -sha1 x.txt
SHA1(x.txt)= a9993e364706816aba3e25717850c26c9cd0d89d
> 
```

#### Multi-block digest

The next step is to compute the size of the message properly and construct a padded message that is an even multiple of the block size.

I separated out the code that does this into a different module:  [pad_sha1.py]([pad_sha1.py).  At this stage I have still not provided an opportunity to pass an arbitrary file to the script.

On the venerable principle of DRY, I tried to fold the code for different versions of SHA into two modules, one for the logic and one for the padding.  But I found it too complicated to wrap my head around the subtle changes from version to version.

Once the message padding worked, the SHA-1 code was modified to allow a multi-block message.  

The example text is Lincoln's Gettysburg Address in `msg2.txt`.  This is nearly 1500 bytes, while the block size is 512 bits (in SHA-1), so there are numerous blocks to be processed.

That code is in [sha1.mod.py](sha1.py).  The last part of the output is:

```
block # 24
final hash:
56c8a390 aba4fae1 7efe6884 97a9665f 39bf7596
```
compare with:

```
> openssl dgst -sha1 msg2.txt 
SHA1(msg2.txt)= 56c8a390aba4fae17efe688497a9665f39bf7596
>
```

#### SHA-256

The next step is SHA-256.  I tried this first on "abc" as before.  It went very smoothly, so I immediately modified the script to process the multi-block message.

```
block # 24
final hash:
90fd6570 a26841f3 57df0bae 475bfd3f 56011b1d ceecc5b8 e0ff4125 99a27af5
> openssl dgst -sha256 msg2.txt 
SHA256(msg2.txt)= 90fd6570a26841f357df0bae475bfd3f56011b1dceecc5b8e0ff412599a27af5
>
```

Looks great!

#### Update

I got SHA-512 working, and everything has been reworked to allow input filenames on the command line.
```
final hash:
ddaf35a193617aba cc417349ae204131 12e6fa4e89a97ea2 0a9eeee64b55d39a 
2192992a274fc1a8 36ba3c23a3feebbd 454d4423643ce80e 2a9ac94fa54ca49f
> openssl dgst -sha512 msg.txt 
SHA512(msg.txt)=
ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a
2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f
>
```

The following output has newlines introduced for readability.
