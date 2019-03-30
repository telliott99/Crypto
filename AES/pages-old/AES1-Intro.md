### Introduction

I've been working on [CryptoPals](https://cryptopals.com), and they want me to implement ECB mode encryption.

I found a tutorial for DES in ECB mode, and implemented it in Python.  

Converting it to CBC mode would be trivial, a top-level wrapper to call it for each block of input, and use of an initialization vector (iv).  See the wikipedia article for details.

Unfortunately, what the CryptoPals want is something that works on 16-bit keys.  DES never uses more than 8-bits.  

What we actually used when we did this from the command line with openssl was AES-128.

So now I need to implement AES.  I don't view the DES thing as a mistake, but just part of the whole learning experience.

### AES with 128-bit keys

I found a nice [source](https://engineering.purdue.edu/kak/compsec/NewLectures/), and several other good sources later.

See lecture 8.  I need to study the other chapters too.  It is math about Galois Fields!

Kak says:

AES (originally Rijndael) uses: 
 
* 128-bit keys (or 128 + 32 * k, where: k = 1,2,3.. )
* the ones > 128 are typically 192 and 256 bits

The encryption consists of 

* 10 rounds of processing for 128-bit keys
* the last round is special

Each round of processing includes

* one single-byte based substitution step, SubBytes
* a row-wise permutation step, ShiftRows
* a column-wise mixing step, MixColumns
* the addition of the round key, AddRoundKey

Regarding the last point:  we will have a key schedule with a different key for each round.

The order in which these four steps are executed is *different* for encryption and decryption.  The way that I got it to work:

* InvShiftRows
* InvSubBytes
* AddRoundKey
* InvMixColumns

However, this is a bit tricky because the design [document]() says some steps are exchangeable.

Before we start the rounds, do a single XOR with the first key in the schedule, for both encryption and decryption.

Kak says to think of the 128-bits as bytes b0 .. b15 arranged in columns:

```
[ b0 b4 b8 b12 ]
[ b1 ..
[ ..
[ ..           ]
```

Thus the first four bits comprise the first column, reading down.

The 4×4 matrix of bytes shown above is referred to as the **state array** in AES.

AES also has the notion of a **word**. A word consists of four bytes, that is, 32 bits.  Each row or column in the state array is a word.  Many of the operations work on one word at a time.

Each round of processing takes an input state array and produces an output state array.

After the last step the output array is rearranged.

### Implementation

Each round carries out each of the following steps (with the exception of the last round).

Also, each step has an inverse method applied during decryption that is somehow different.  For example, there is a different S-box for decryption.  Also, during decryption the steps are followed in inverse order.

#### Substitution

This is byte by byte substitution using a 16 x 16 lookup table called an S-box, familiar to us from DES.  The same box is used in all 10 rounds.  The operation is similar as well:

> To find the substitute byte for a given input byte, we divide the input byte into two 4-bit patterns, each yielding an integer value between 0 and 15.

> The S-box ensures that *every* input byte is mapped to a different and unique output byte.  At no position does the input byte map to the same byte.  This is important for a strong cipher.

We will work out the details of the lookup later.  I copied both the encrypt and decrypt S-box from the source and proofed them.

#### Shift Rows

* row 0 is not shifted
* row 1 is shifted 1 position left
* row 2 is shifted 2
* row 3 is shifted 3

Recall that the input block is written-column wise

```
s00 s01 s02 s03
s10 s11 s12 s13
s20 s21 s22 s23
s30 s31 s32 s33
```

After the row shift we obtain

```
s00 s01 s02 s03      s00 s01 s02 s03
s10 s11 s12 s13  ->  s11 s12 s13 s10
s20 s21 s22 s23      s22 s23 s20 s21
s30 s31 s32 s33      s33 s30 s31 s32
```

Writing the block column-wise and then shifting rows scrambles the block except for the top row, of course.  The numerical order is transformed:

```
0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
0 13 10  7  4  1 14 11  8  5  2 15 12  9  6  3
```

Another way to look at this would be to say that we can do byte look-up by that schedule.

#### Mix Columns

These steps (and the construction of the S-boxes) use what Kak calls GF(2<sup>n</sup>) arithmetic, explained in chapter 7 of his course notes.

My notes on arithmetic for Galois Fields based on his notes are [here](../../AES-math/README.old.md).

We use lookup tables similar to what is in the wikipedia [article](https://en.wikipedia.org/wiki/Rijndael_mix_columns).  

Using Kak's explanations, I've written code to construct tables, and these are identical to those in the wikipedia article. 

> The shift-rows step along with the mix-column step causes each bit of the ciphertext to depend on every bit of the plaintext after 10 rounds of processing.

* The last round for encryption does not do the **MixColumns** step

#### Add Round Key

On page 10 Kak says:

> The last step consists of XORing the output of the previous three steps with four words from the key schedule.

#### Decryption note:

For decryption the steps are:

* InvShiftRows
* InvSubBytes
* AddRoundKey
* InvMixColumns

The last round for decryption does not do the last step.

We continue with a discussion of the math [here](AES-math.md).

The description of how to produce a 44 x 4-byte key schedule from a 4 x 4-byte key is [here](AES-key.md).

