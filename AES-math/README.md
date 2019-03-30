This project is about the math used for AES (advanced encryption standard).  I worked it all out a couple of years ago, but found it quite confusing when I went back.  

The goal now is to make it understandable the next time I come back.

The short answer is this:  what all of this mathematics amounts to is it produces a **particular permutation** of the integers 0-255 which is a Galois field GF(2<sup>8</sup>).  That's it.

This particular permutation is special, when interpreted by the Galois field rules, the integers can be grouped into pairs that are "multiplicative inverses".  This is not standard multiplication.

#### Operations

The mathematical operations for this field are summarized [here](pages/operations.md).

#### Code 

The code for this part of the AES project is in ``core-code/``.  There is a [README](code/README.md) file.

#### Theory of Galois Fields

- Intro to [modular arithmetic](pages/modular-arithmetic.md)
- Defining a [field](pages/field.md)

Inpdftermediate (pdf makes it easier to typeset math):

- [Galois fields](pdfs/Galois-fields.pdf)
- [Polynomial](pdfs/polynomials.pdf) arithmetic
- more [Galois fields](pdfs/GF(2e8).pdf)

Continuing with markdown:

#### Constructing our GF

- [Constructing](pages/galois-field.md) GF(2<sup>8</sup>)
- [generators](pages/primitive-elements.md)

An aside, but we explore the property of irreducibility.

- [checking irreducibility](pages/irreducible.md)

I wrote a simple, short Python script to carry out multiplication over the field GF(2<sup>8</sup>.  Using that, we can generate the elements of the field as powers of a primitive element like ``0x03`` (there are other primitive elements).

The powers are just a table of exponents of the generator ``0x03``:  for each index i into the array, ``g^i = n``, where ``n`` is the value at the index.  

Turning this around, ``i`` is the logarithm of ``n`` to the power ``g``.  Reverse the table to make a new table of discrete logarithms.  The logarithms can be used for multiplication.  Simply add two logs and look up the result in the original exp table.

Having done all of that, we can generate a table of multiplicative inverses.  We will need those for AES, as well as the ability to multiply any byte by the small numbers 2, 3, 9, 11, 13, 14.

I checked the table of multiplicative inverses against my multiplication function, and found a bug.  The bug did not affect multiplication by 3, so all the tables checked out, but the mod operation was incorrect for any product >= 512. I fixed the bug and retested.

- [problem](pages/mod-problem.md) with mod

I also worked out

- matrix [inversion](pages/inversion.md)
 
#### Archive

These were originally developed as writeups in the ``pdfs.old`` directory, reading in this order

- [Finite_fields.pdf](pdfs.old/Finite_fields.pdf)
- [GF(2e8).pdf](pdfs.old/GF(2e8).pdf)
- [Generators.pdf](pdfs.old/Generators.pdf)
- [Generators2.pdf](pdfs.old/Generators2.pdf)

