### Math for AES

The MixColumns step and one step of the key expansion (as well as the construction of the S-boxes) use what Kak calls GF(2<sup>n</sup>) arithmetic (GF stands for Galois Field).  

This is explained in [Chapter 7](https://engineering.purdue.edu/kak/compsec/NewLectures/Lecture7.pdf) of his course notes.  I also have a write-up about it in AES-math notes.

One would guess, of course, that our specific interest is GF(2<sup>8</sup>) or 0..255, and that is correct. 

My initial problem was that I hadn't understood how to do the multiplications after browsing through Chapter 7.  So the first part of this page explains how to *bypass* that issue.

### Practical solution

Wikipedia has a whole [article](https://en.wikipedia.org/wiki/Rijndael_mix_columns) on the MixColumns step.

In the article they have Galois multiplication lookup tables.  Unlike the S-boxes, which when I copied from the pdf had haphazard spacing, these tables cut and paste beautifully [Update:  they seem to have been removed from the article, my copies are [here](../AES/AES-code/old/aes_info.py)].

About the S-boxes, if I were doing this again, I should have gone to the official U.S. government spec [here](http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf). 

[Update: that pdf is no longer on the web, but I found a copy of it [here](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)]. So I downloaded it, it is in this directory. 

The S-box tables on pg. 16 and pg. 22 cut and paste nicely (if you do it in two parts above and below the "x").

The tables are for multiplication by 2 and so on.  The beginning is ``0x00,0x02`` etc.  The data is comma separated hex values, with 256 entries in each table.  

To multiply a byte by 2 you simply look up the value at that index in ``x2``.

Altogether, there are tables for 2, 3, 9, 11, 13 and 14.  I put them in the sub-directory:  ``tables``.  For encryption, we need only 2x and 3x, but for decryption we need the other four.

Multiplication is one 4-byte **word** at a time.  To do this we use a matrix, as you'd expect. 

In the forward direction, the transformation matrix is:

```
matrix_encrypt = '''
2  3  1  1
1  2  3  1
1  1  2  3
3  1  1  2
'''
```

Going the other way

```
matrix_decrypt = '''
14 11 13  9
 9 14 11 13
13  9 14 11
11 13  9 14
'''
```
I saved these matrices in **aes_info** as ``'matrix_encrypt.txt'``.  

So if the input word is [a<sub>0</sub> , a<sub>1</sub>, a<sub>2</sub>, a<sub>3</sub>], the result is

b<sub>0</sub> = 2 a<sub>0</sub> &#8853; 3 a<sub>1</sub> &#8853; a<sub>2</sub> &#8853; a<sub>3</sub>

b<sub>1</sub> = a<sub>0</sub> &#8853; 2 a<sub>1</sub> &#8853; 3 a<sub>2</sub> &#8853; a<sub>3</sub>

b<sub>2</sub> = a<sub>0</sub> &#8853; a<sub>1</sub> &#8853; 2 a<sub>2</sub> &#8853; 3 a<sub>3</sub>

b<sub>3</sub> = 3 a<sub>0</sub> &#8853; a<sub>1</sub> &#8853; a<sub>2</sub> &#8853; 2 a<sub>3</sub>


The wikipedia article also gives five examples of input and output:

```
db 13 53 45 -> 8e 4d a1 bc
f2 0a 22 5c -> 9f dc 58 9d
01 01 01 01 -> 01 01 01 01
c6 c6 c6 c6 -> c6 c6 c6 c6
d4 d4 d4 d5 -> d5 d5 d7 d6
2d 26 31 4c -> 4d 7e bd f8
```

and they give the same six examples in decimal:

```
219  19  83  69 -> 142  77 161 188
242  10  34  92 -> 159 220  88 157
  1   1   1   1 ->   1   1   1   1
198 198 198 198 -> 198 198 198 198
212 212 212 213 -> 213 213 215 214
 45  38  49  76 ->  77 126 189 248
```

I wrote Python code which can do this.  The original  version was based on the wikipedia tables.  All 6 examples worked.  

Then I added a decrypt mode and showed that I get the input back.

After that, I figured out how to construct my own lookup tables, and then I wrote code to generate them.  I made tables with both int and hex values.  I used the int ones in my code.  Currently, we use hex.

I re-worked the code to do the examples and put it in.

I tested that random input is equal to the result of encrypt followed by decrypt, for 100,000 runs.

This is all you really need to carry out AES.  However, I'm trying to get a better handle on the math involved.