TL;DR

Irreducible"

``` 
degree 1:     11    10
degree 2:    111
degree 3:   1011  1101
degree 4:  10011 11001 11101 11111
..
..
..
100011011
```

How to prove that last part?

#### Irreducibility

How to prove that ``x^8 + x^4 + x^3 + x + 1`` is *irreducible*?

This is ``1 0001 1011 = 100011011``. 

So the contrary is that two polynomials multiplied together give this as the result, if so, then one at least must be of degree 4 or less since ``x^4 * x^4 = x^8``.  

We could generate all the polynomials of degree 4 or less and check them by polynomial division.  That's ``2^5 + 2^4 + 2^3 + 2^2 + 2`` = 63 

(the NCAA basketball tournament problem).

There's another way.  If the number above *is* reducible, then its factors are irreducible polynomials.  

We can generate all of them.  There are 9, and they are written above.  We've seen all of them except those of degree 4 before.

Let's find those, and then test the "irreducible polynomial".

As a warmup, determine all the irreducible polynomials of degree 3 or less:

#### degree 1

```
10 = x
11 = x + 1
```

#### degree 2

Pairwise multiplication of degree 1 gives degree 2

```
100 = x^2
110 = x * (x + 1) = x^2 + x
101 = (x + 1) * (x + 1) = x^2 + 1
```
These 3 are reducible.  What's left?  There are 4 total.

```
111 = x^2 + x + 1 must be irreducible
```

Check by trial division:

```
111
10
--
 11
 10
 -- 
  1 r
  
111
11
--
  1 r

```

#### degree 3

Multiply all degree 2's by all degree 1's.

```
1000 = x^3
1100 = x^3 + x^2
1010 = x^3 + x
1110 = x^3 + x^2 + x

1100 = (x + 1) * x^2 = x^3 + x^2
1010 = (x + 1) * (x^2 + x) = x^3 + x
1111 = (x + 1) * (x^2 + 1) = x^3 + x^2 + x + 1
1001 = (x + 1) * (x^2 + x + 1) = x^3 + 1
```

There are 6 unique ones.  It's easier to see if we write them as binary numbers.

```
1000 1100 1010 1110 1111 1001
```

Rearrange:

```
1000 1001 1010
1100 1110 1111
```

What's missing?  ``1011`` and ``1101``.

Therefore the two irreducibles at degree 3 are:

```
1011 = x^3 + x + 1
1101 = x^3 + x^2 + 1
```

These can also be written:

```
x^3 + x + 1
x^3 + x^2 + 1
```

Check by trial division.  

We could test against all 4 degree 2's.

Because it is degree 3, one degree 2 must be a factor (along with a degree 1).  Alternatively, at least one degree 1 must be a factor.

First: ``x^3 + x + 1 = 1011``

```
#1
1011
100
 ---
 011 r
 
#2
1011
101
 ---
 001 r
 
#3
1011
110
 ---
 111 
 110
 ---
   1 r
 
#4
1011
111
 ---
 101
 111
 ---
  10 r
 ```

Next: ``x^3 + x^2 + 1 = 1101``

```
#1
1101
100
 ---
 101
 100
 ---
   1 r
 
#2
1101
101
 ---
 111 
 101
 ---
  10 r
 
#3
1101
110
 ---
   1 r
 
#4
1101
111
 ---
  11 r
 ```

We've confirmed the two postulated irreducibles at degree 3.

#### degree 4

Self-multiply all four degree 2.

```
            100    101    110    111
100 x ->  10000         
101 x     10100  10001      
110 x     11000  11110  10100 
111 x     11100  11011  10010  10101
```

One dup (``10100``).

Also multiply all eight degree 3 by all degree 1:

```
              10     11
1000 x ->  10000  11000        
1001 x     10010  11011   
1010 x     10100  10001 
1011 x     10110  11011
1100 x ->  11000  10100      
1101 x     11010  10111   
1110 x     11100  10010
1111 x     11110  10001
```

Figure out what's missing...

```
10000 10001 10010 10011 10100 10101 10110 10111
x     x     x           x     x     o     o     

11000 11001 11010 11011 11100 11101 11110 11111
x           o     x     x           x
```

So I seem to have four:

```
10011 11001 11101 11111
```

#### Trial division

Take all irreducible polynomials of any degree and try to divide the "irreducible" polynomial

Start with the degree 4 irreducibles, and use the trick approach to division:

```
#1
100011011
10011
-----
   101011
   10011
   -----
     1101 r

#2
100011011
11001
-----
 10001011
 11001
 -----
  1000011
  11001
  -----
   100111
   11001
   -----
    10101
    11001
    -----
     1100 r

#3
100011011
11101
-----
 11001011
 11101
   -----
   100011
   11101
   -----
    11001
    11101
    -----
      100 r

#4
100011011
11111
-----
 11101011
 11111
   -----
    10011 
    11111
    -----
     1100 r
```

Degree 3 and smaller are five:

```
1101
1011
111
10
11
```

Try them all

```
#1
100011011
1101
----
 10111011
 1101
 ----
  1101011
  1101
  ----
      011 r
      
#2
100011011
1011
----
  1111011
  1011
  ----
   100011
   1011
   ----
     1111
     1011
    -----
      100 r

#3
100011011
111
----
 11011011
 111
 ---
   111011
   111
   ---
      011 r

#4
100011011
10
----
    11011
    10
    ----
     1011
     10
     ----
       11
       10
       --
        1 r

#5
100011011
11
--
 10011011
 11
 --
  1011011
  11
  --
   111011
   11
   --
     1011
     11
     --
      111
      11
      --
        1 r
```

Checking the last one again, we're asking if ``x + 1`` divides 

```
x^8 + x^4 + x^3 + x + 1
(x+1) * x^7 = x^8 + x^7 XOR above -> 
x^7 + x^4 + x^3 + x + 1
(x+1) * x^6 = x^7 + x^6 XOR above -> 
x^6 + x^4 + x^3 + x + 1
(x+1) * x^5 = x^6 + x^5 XOR above -> 
x^5 + x^4 + x^3 + x + 1
(x+1) * x^4 = x^5 + x^4 XOR above -> 
x^3 + x + 1
(x+1) * x^2 = x^3 + x^2 XOR above ->
x^2 + x + 1
(x+1) * x = x^2 + x XOR above ->
r = 1
```

So, no, it doesn't.

There's got to be a better way.  We can do the graphical method:

```
100011011
11
--
 10011011
 11
 --
  1011011
  11
  --
   111011
   11
   --
     1011
     11
     -- 
      111
      11
      --
        1 r
```

Another way is to code it.  I wrote a script with a function called [string_division](../code-core/str_div.py) which does "string" division.  

Given the irreducible polynomial as ``'100011011'`` and any of the irreducibles up to degree 4 as

```
L = ['10','11',
     '111',
     '1011','1101',
     '10011', '11001', '11101', '11111']

```

it prints something like

```
string division
 100011011
 11001
  10001011
  11001
   1000011
   11001
    100111
    11001
     10101
     11001
      1100
result:  1100
```

Comparing the output with the calculations I did by hand above, I found four errors, and one bug!

I also found 30 irreducible polynomials of degree 8.  Here are the first four:

```
100011011
100011101
100101011
100101101
..
```

You will recognize our old friend as the first one, with the smallest binary representation.