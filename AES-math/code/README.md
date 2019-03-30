The core logic is in 

- [gmath.py](gmath.py)

I/O is in 

- file_io.py

Print formatting is in 

- fmt.py

Dictionary construction is in 

- [gdict.py](gdict.py)

[``make.py``](make.py) constructs int and hex versions of two tables:  powers of the generator, and logarithms.  The powers are also antilogs.  These are written to disk

The code can easily be modified to use a different generator ("primitive element") and also a different "irreducible polynomial".

The output tables have been placed in ``/tables`` as ``g3.powers`` and ``g3.logs``.  Each comes in two versions:  ``xx.int.txt`` and ``xx.hex.txt``.  It made testing easier to leave copies of the main ones at the top level even though this violates DRY.

The hex output can be compared by eye with the screenshots from Wagner, Laws of Cryptography.

``make_mi.py`` uses the log table to construct a table of multiplicative inverses.

Run the test.sh script by dragging the icon to the Terminal.  

It will build a tmp directory on the Desktop and run the tests there.  To erase it just do ``rm -rf tmp``, or drag it to the Trash.
