Two of my sources are

- [Kak](https://engineering.purdue.edu/kak/compsec/Lectures.html)
- [Wagner](http://www.cs.utsa.edu/~wagner/laws/FFM.html)

We start with some notes from the first source, early chapters from Prof. Kak's course on cryptography.

### Definitions

#### Group

A **group** G is a set of objects plus a binary operation (operator o), with the following properties.  If a,b &#8712; G, the operations exhibit:


- Closure:  ``a o b = c`` &rightarrow; ``c in G``
- Associativity:  ``(a o b) o c = a o (b o c)``
- Identity element:  ``a o i = a``
- Inverse element:   ``a o b = i``

A common notation is to use ``{G,+}``, (``+`` for the operator, even if the operation is not really like addition).  

If ``a + i = a``, call ``i`` the identity element and typically use ``0`` as the symbol for it.

#### Abelian Group

An Abelian group is:

- Commutative:  ``a o b = b o a``

for addition.

#### Ring

A **ring** is a group with the multiplication operator ``*``, (even if the operation is not really like multiplication).

Actually, the ``x`` symbol is more common, but I'm following Python notation.  And in fact, it is common to drop the ``*`` as in ``ab`` or ``a(b+c)``.

A ring may be designated as ``{R,+,*}`` and exhibits:

- Closure:  ``ab in R``
- Associativity:  ``(ab)c = a(bc)``
- Distributivity:  ``a(b + c) = (ac) + (ab)``

A ring *may* be 

- Commutative:    ``ab = ba``

for multiplication, but not necessarily.

An integral domain  is a commutative ring that also has a

- Multiplicative identity element: ``a*1 = a``

If ``ab = 0``, then either ``a = 0`` or ``b = 0``.

#### Field

A **field** {F,+,*} is an integral domain that has, for every ``a`` a multiplicative inverse ``b``

- Multiplicative inverse: ``ab = 1``

``1`` is its own multiplicative inverse.

According to [wikipedia](https://en.wikipedia.org/wiki/Finite_field)

> In mathematics, a finite field or Galois field ... is a field that contains a finite number of elements. As with any field, a finite field is a set on which the operations of multiplication, addition, subtraction and division are defined and satisfy certain basic rules.

You can read all about it there.  I *think* this conveys the general idea and is enough to get started.