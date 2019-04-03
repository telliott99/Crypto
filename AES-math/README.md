This project is about the math used for AES (advanced encryption standard).  I worked it out a couple of years ago, but found it quite confusing when I went back.  

The goal now is to make it understandable the next time I come back.

The short answer is this:  what all of this mathematics amounts to is a **particular permutation** of the integers 1-255 which is a Galois field GF(2<sup>8</sup>).  That's it.

This particular permutation is special, when interpreted by the Galois field rules, the integers can be grouped into pairs that are "multiplicative inverses".  This is not standard multiplication.

And the succession of values can be written as powers of a generator or primitive element like ``0x03``.

#### Operations

The mathematical operations for the field are summarized [here](pages/operations.md).

#### Code 

The code for this part of the AES project is in ``core-code/``.  There is a [README](code/README.md) file.

#### Theory of Galois Fields

- Intro to [modular arithmetic](pages/modular-arithmetic.md)
- Defining a [field](pages/field.md)

To some extent, there are parallel expositions in markdown and pdf.  The markdown is closely linked to Python code and less theoretical.

In pdf format (pdf makes it easier to typeset math):

- [Galois fields](pdfs/1-Galois-fields.pdf)
- [Finite fields](pdfs/2-Finite_fields.pdf) arithmetic
- [Polynomial](pdfs/3-polynomials.pdf) arithmetic
- [GF(2^3)](pdfs/4-GF(2e3).pdf)
- [GF(2^4)](pdfs/5-GF(2e4).pdf)
- [GF(2^8)](pdfs/6-GF(2e8).pdf)
- [Generators)](pdfs/Generators.pdf)
- [more Generators](pdfs/Generators2.pdf)

Continuing with markdown:

#### Constructing GF(2e8)

- [Constructing](pages/galois-field.md) GF(2<sup>8</sup>)
- [generators](pages/primitive-elements.md)

An aside, but we explore the property of irreducibility.

- [checking irreducibility](pages/irreducible.md)

I wrote a pair of simple, short Python [functions](code/gmath.py) to carry out multiplication and the mod operation over the field GF(2<sup>8</sup>.  

Using that, we can generate the elements of the field as powers of a primitive element like ``0x03`` (there are other primitive elements).

The powers are just a table of exponents of the generator ``0x03``:  for each index i into the array, ``g^i = n``, where ``n`` is the value at the index.  

Turning this around, ``i`` is the logarithm of ``n`` to the power ``g``.  Reverse the table to make a new table of discrete logarithms.  The logarithms can be used for multiplication.  Simply add two logs and look up the result in the original exp table.

Having done all of that, we can generate a table of multiplicative inverses.  We will need those for AES, as well as the ability to multiply any byte by the small numbers 2, 3, 9, 11, 13, 14.

#### small bug

I checked the table of multiplicative inverses against my multiplication function, and found a bug.  The bug did not affect multiplication by 3, so all the tables checked out, but the mod operation was incorrect for any product >= 512. I fixed the bug and retested.

- [problem](pages/mod-problem.md) with mod

I mention this because some of the early write-ups may not have been corrected for this.

I also worked out a matrix multiplication routine

- matrix [inversion](pages/inversion.md)

which explains why the particular matrices used for encryption and decryption in AES are as they are (namely, their product is the identity matrix, I).