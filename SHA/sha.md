#### Introduction

I mainly used the official NIST doc [fips180-2.pdf](http://csrc.nist.gov/publications/fips/fips180-2/fips180-2.pdf), and a subsequent version as well [fips180-4.pdf](http://csrc.nist.gov/publications/fips/fips180-4/fips180-4.pdf).

But there is a lot of additional explanation in [Kak](https://engineering.purdue.edu/kak/compsec/NewLectures/Lecture15.pdf).

#### Utility functions

Functions for operations on bits (mainly wrappers for Python bit operations) are in [bits.py](bits.py).

These include two print functions:

* `pprint(L)` to print a list
* `pbin(x)` to print bin, hex, int and 'x' for `x`

The bit-manipulation functions are

* `AND`
* `XOR`
* `OR`
* `NOT`
* `ADD`
* `SHR` (right-shift)
* `SHL` (left-shift)
* `ROTR` (`SHR`, with rotation)
* `ROTL` (`SHL`, with rotation)

I should mention that I decided again to follow the advice of CryptoPals, and implement all of these functions with integers.

I would have used the `UInt8` type if using Swift, but Python does so well with large numbers that I just let it do the heavy lifting.

We convert to hex or binary for output, as needed.

A notable feature is that `AND`, `XOR`, `OR` and `ADD` can take a variable number of arguments.

This may be a good place to say that I implemented `OR` because of [this reference](https://en.wikipedia.org/wiki/SHA-1#SHA-1_pseudocode), which shows both `OR` and `XOR` in the main loop.  I did this when I couldn't get my version to work, at first. 

However, that reference is incorrect.  All calls should be `XOR`, as the NIST standard has it.

#### Additional functions

Then, there are three functions used across all the SHA implementations:

* `Ch(x,y,z)`
* `Maj(x,y,z)`
* `Parity(x,y,z)`

Parity is simply `XOR` of the 3 values, so at any place the result is `1` if the number of `1`'s in the arguments is odd.  (Note:  the symbol &#8853; is often used for XOR, but it doesn't work inside the quoted environment here, and I prefer to keep non-ASCII characters out of my script files.

```
Maj(x,y,z) = (x ^ y) XOR (x ^ z) XOR (y ^ z)
Ch(x,y,z) = (x ^ y) XOR (~x ^ z)
```

The `NOT` symbol (`~`) in `Ch` is missing in [this reference](http://csrc.nist.gov/publications/fips/fips180-2/fips180-2.pdf) (p. 9).  And actually, in the other version they use a different symbol that I haven't found in html yet.

There are also additional functions that will become important later, but they are not used for SHA-1.

An important resource for this project is the correct output for different variables at each stage of the algorithm.  The original NIST doc ([fips180-2.pdf](http://csrc.nist.gov/publications/fips/fips180-2/fips180-2.pdf)) has the values of the variables `a-e` for each stage, although not the rest of the detail.

Also, those examples are deleted in the current version.  I'm not sure why, but it's too bad.

A great help in debugging was to find this [site](http://www.metamorphosite.com/one-way-hash-encryption-sha1-data-software) on the web, which generates the precise output of every step for any input.  

That was wonderful, and helped me track down the last bug.

Let's take a look.

#### Padding the message

The basic idea is pretty simple.  We want the message to be a multiple of the block size.  For SHA-1 and SHA-256, the block size is 512 bits, for SHA-512, it is 1024 bits.

Our simple example message is `abc`, which is 3 bytes or 24 bits.  We encode that size in hex as `18` and place that value as the last 64-bit word of the message (128 bits for SHA-512).

We can calculate that the last 9 bits are not `0` (8 bits plus one more for `1`).

In addition, the bit just after the end of our data should be `1`, followed by as many zeros as are needed.  I calculate:  

```
512 - 25 - 5 = 482
```

The NIST/fips reference gives this number as 423 `0`'s plus 64 bits ending in `11000`.  So that's 423 + 59 = 482.  It checks.

#### Message schedule

For each block, we start with 512 bits organized as 16 32-bit words.  These 16 values are expanded to give a total of 80 words, one for each of the 80 rounds of the computation that happens for every block.  

This is called the message schedule.  I called it the word list, `wL`.

For SHA-1, the formula to generate the `ith` value is to do

```
ROTL( XOR(L),5 )
```

where

```
L = [wL[i-3], wL[i-8], wL[i-14], wL[i-16]]
```

the formulas are different for other versions of SHA.

#### Hash values

For SHA-1, there are five variables that are initially set to be magic numbers:

```
H0 = 67452301H1 = efcdab89H2 = 98badcfe
H3 = 10325476
H4 = c3d2e1f0
```

I am not clear on where these particular values come from for SHA-1, but for SHA-256 and SHA-512, there are 8 of them, and they are derived from the square roots of the first 8 prime numbers, as described [here](sha-magic.md).

We will initialize variables `a` through `e` with these values, each time through the inner loop (which runs 80 times) `a-e` are modified.

At the very end, the initial values must be recalled.  The last step is to compute `a + H0`, etc., where `H0 = 67452301`, and so on.

#### Functions and constants

Another wrinkle is that each round of the inner loop uses a different magic constant `K`, derived from the *cube* roots of the first 80 primes, as  described [here](sha-preliminary.md).

The functions used in the inner loop are

* round 0-19: &nbsp;  `Ch`
* round 20-39: `Parity`
* round 40-59: `Maj`
* round 60-79: `Parity`

#### Inner loop

* Compute `ROTL(a,5)`
* Compute `f(b,c,d)` 

where `f` is determined as described in the last section.  Then compute 

``` 
T = ADD( ROTL(a,5), f(b,c,d), e, K, W )
```

where `K` and `W` are the constant and word for the current round.

Make new assignments to the working variables, in this order

* e = d
* d = c
* c = ROTL(b,30)
* b = a
* a = T

That's the end of the inner loop.

#### Last step

The last step is to compute

* `AND(a, H0)`
* `AND(b, H1)`
* etc.

#### Verify the ouput

The script is [sha1.py](sha1.py).

The last line of the output is

```
a9993e36 4706816a ba3e2571 7850c26c 9cd0d89d
```

which does indeed match `openssl`:

```
> printf "abc" > x.txt
> openssl dgst -sha1 x.txt
SHA1(x.txt)= a9993e364706816aba3e25717850c26c9cd0d89d
> 
```

I went on to implement SHA-256 and SHA-512 and detailed output from the runs on two message files, along with comparison with what `openssl` gives, are in the `results` folder.  Happy hashing!