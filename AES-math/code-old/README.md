- aes_utils.py 

is a more or less up-to-date copy of what is in the pyaes project.  I kept a local copy to use readData to load data.

Code of intermediate age using the 0x03 generator is in the /old directory 

- make_expL.py
- make_logL.py
- make_MI.py

which make respectively, the powers of 0x03, the logs, and find multiplicative inverses.

Later I combined these and printed a single table, so the version at top-level is the latest:

- make_all.py
- all.x3tables.txt

-----------------------

- find_generator.py is a quickie script to do what it says.  With it I discovered that generators are actually pretty common.

-----------------------

Still older code is in the /galois directory.

- galois_hex.py contains hex times tables for 2,3,9,11,13,14 made by

- make_galois_tables.py

That script has original versions of code for doing multiplication in GF(2e8) the standard way, breaking one multiplicand into powers of two, etc.

The original pasted tables from wikipedia are in

- wiki_tables.py

-----------------------

Latest approaches of how to do multiplication are in

- make_all.py

but only times2 and times 3 are there b/c I just started using logarithms

-----------------------

The latest thing is to write a script 

- wagner.py

to do calculations as described [here](http://www.cs.utsa.edu/~wagner/laws/FFM.html).  I have a post about this [here](https://telliott99.blogspot.com/2017/01/generator-for-galois-field.html)

- multiply.py

used like this:

```
> python multiply.py hex ca 53
x 202 y 83 p 1 01
>
```

Finally, following Kak

- make_Sboxes.py

twiddles bits to make the S-box for encryption.  Basically, starting from the index into the range(256) you:

- get the multiplicative inverse
- shift right 4
- shift right 5
- shift right 6
- shift right 7

XOR all that and then XOR with the magic bye **0x63**.

The result matches my source.