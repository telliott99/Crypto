### AES

#### Encryption

Now that we've figured out how to do the MixColumns step and generate the key schedule, we're ready to try encryption.

I'm going to follow this [source](https://kavaliro.com/wp-content/uploads/2014/03/AES.pdf), primarily because it has detailed output for each step.

The key is:

```
'Thats my Kung Fu'
54 68 61 74 73 20 6d 79 20 4b 75 6e 67 20 46 75
5468617473206d79204b756e67204675
```

The plaintext is

```
'Two One Nine Two'
54 77 6f 20 4f 6e 65 20 4e 69 6e 65 20 54 77 6f
54776f204f6e65204e696e652054776f
```

We put that into a file simply by

```
> echo -n "Two One Nine Two" > msg.txt
> hexdump -C msg.txt
00000000  54 77 6f 20 4f 6e 65 20  4e 69 6e 65 20 54 77 6f  |Two One Nine Two|
00000010
>
```

and read it into our Python script with

```python
>>> import utils as ut
>>> ut.readData('msg.txt')
'Two One Nine Two'
>>>
```

We anticipate what the result should be with

```
> openssl aes-128-ecb -e -nopad -K "5468617473206d79204b756e67204675" -in msg.txt | xxd -p
29c3505f571420f6402299b31a02d73a
> 
```

And it works!

```python
> python aes.py
key schedule:
 0         54 68 61 74 73 20 6d 79 20 4b 75 6e 67 20 46 75
 1         e2 32 fc f1 91 12 91 88 b1 59 e4 e6 d6 79 a2 93
 2         56 08 20 07 c7 1a b1 8f 76 43 55 69 a0 3a f7 fa
 3         d2 60 0d e7 15 7a bc 68 63 39 e9 01 c3 03 1e fb
 4         a1 12 02 c9 b4 68 be a1 d7 51 57 a0 14 52 49 5b
 5         b1 29 3b 33 05 41 85 92 d2 10 d2 32 c6 42 9b 69
 6         bd 3d c2 87 b8 7c 47 15 6a 6c 95 27 ac 2e 0e 4e
 7         cc 96 ed 16 74 ea aa 03 1e 86 3f 24 b2 a8 31 6a
 8         8e 51 ef 21 fa bb 45 22 e4 3d 7a 06 56 95 4b 6c
 9         bf e2 bf 90 45 59 fa b2 a1 64 80 b4 f7 f1 cb d8
10         28 fd de f8 6d a4 24 4a cc c0 a4 fe 3b 31 6f 26

key:       54 68 61 74 73 20 6d 79 20 4b 75 6e 67 20 46 75
data:      54 77 6f 20 4f 6e 65 20 4e 69 6e 65 20 54 77 6f
round  0:  00 1f 0e 54 3c 4e 08 59 6e 22 1b 0b 47 74 31 1a
round  1:  58 47 08 8b 15 b6 1c ba 59 d4 e2 e8 cd 39 df ce
round  2:  43 c6 a9 62 0e 57 c0 c8 09 08 eb fe 3d f8 7f 37
round  3:  78 76 30 54 70 76 7d 23 99 3c 37 5b 4b 39 34 f1
round  4:  b1 ca 51 ed 08 fc 54 e1 04 b1 c9 d3 e7 b2 6c 20
round  5:  9b 51 20 68 23 5f 22 f0 5d 1c bd 32 2f 38 91 56
round  6:  14 93 25 77 8f a4 2b e8 c0 60 24 40 5e 0f 92 75
round  7:  53 39 8e 5d 43 06 93 f8 4f 0a 3b 95 85 52 57 bd
round  8:  66 25 3c 74 70 ce 5a a8 af d3 0f 0a a3 73 13 54
round  9:  09 66 8b 78 a2 d1 9a 65 f0 fc e6 c4 7b 3b 30 89
round 10:  29 c3 50 5f 57 14 20 f6 40 22 99 b3 1a 02 d7 3a
ciphertxt: 29 c3 50 5f 57 14 20 f6 40 22 99 b3 1a 02 d7 3a
>
```

I now have the whole thing working, at least for this key:

```bash
key schedule:
 0         54 68 61 74 73 20 6d 79 20 4b 75 6e 67 20 46 75
 1         e2 32 fc f1 91 12 91 88 b1 59 e4 e6 d6 79 a2 93
 2         56 08 20 07 c7 1a b1 8f 76 43 55 69 a0 3a f7 fa
 3         d2 60 0d e7 15 7a bc 68 63 39 e9 01 c3 03 1e fb
 4         a1 12 02 c9 b4 68 be a1 d7 51 57 a0 14 52 49 5b
 5         b1 29 3b 33 05 41 85 92 d2 10 d2 32 c6 42 9b 69
 6         bd 3d c2 87 b8 7c 47 15 6a 6c 95 27 ac 2e 0e 4e
 7         cc 96 ed 16 74 ea aa 03 1e 86 3f 24 b2 a8 31 6a
 8         8e 51 ef 21 fa bb 45 22 e4 3d 7a 06 56 95 4b 6c
 9         bf e2 bf 90 45 59 fa b2 a1 64 80 b4 f7 f1 cb d8
10         28 fd de f8 6d a4 24 4a cc c0 a4 fe 3b 31 6f 26


Encrypt
input:     54 77 6f 20 4f 6e 65 20 4e 69 6e 65 20 54 77 6f
round  0:  00 1f 0e 54 3c 4e 08 59 6e 22 1b 0b 47 74 31 1a

key:       54 68 61 74 73 20 6d 79 20 4b 75 6e 67 20 46 75
round  1:  58 47 08 8b 15 b6 1c ba 59 d4 e2 e8 cd 39 df ce
round  2:  43 c6 a9 62 0e 57 c0 c8 09 08 eb fe 3d f8 7f 37
round  3:  78 76 30 54 70 76 7d 23 99 3c 37 5b 4b 39 34 f1
round  4:  b1 ca 51 ed 08 fc 54 e1 04 b1 c9 d3 e7 b2 6c 20
round  5:  9b 51 20 68 23 5f 22 f0 5d 1c bd 32 2f 38 91 56
round  6:  14 93 25 77 8f a4 2b e8 c0 60 24 40 5e 0f 92 75
round  7:  53 39 8e 5d 43 06 93 f8 4f 0a 3b 95 85 52 57 bd
round  8:  66 25 3c 74 70 ce 5a a8 af d3 0f 0a a3 73 13 54
round  9:  09 66 8b 78 a2 d1 9a 65 f0 fc e6 c4 7b 3b 30 89
round 10:  29 c3 50 5f 57 14 20 f6 40 22 99 b3 1a 02 d7 3a
ciphertxt: 29 c3 50 5f 57 14 20 f6 40 22 99 b3 1a 02 d7 3a


Decrypt
input:     29 c3 50 5f 57 14 20 f6 40 22 99 b3 1a 02 d7 3a
round  0:  01 3e 8e a7 3a b0 04 bc 8c e2 3d 4d 21 33 b8 1c

key:       54 68 61 74 73 20 6d 79 20 4b 75 6e 67 20 46 75
round  1:  33 8b 76 20 51 66 7d 92 79 8f eb c2 0a 3f be 67
round  2:  ed 6f e2 7a 1a 67 5b 4c 84 00 19 41 97 12 dc 2a
round  3:  fa 49 36 9d 73 d0 4f f5 ba 76 3f 9b 58 dc f1 09
round  4:  14 cf 7a b1 26 9c 81 45 4c 07 b7 8c 15 d1 93 23
round  5:  c8 b0 dd b7 30 c8 50 55 f2 37 d1 f8 94 74 20 66
round  6:  bc 38 9a a1 51 eb 18 20 ee 12 04 26 b3 38 ff 39
round  7:  1a 5b e9 9a ab 30 d2 aa 01 41 d3 e8 27 b4 ba bb
round  8:  6a 4e 98 8b 59 48 9e 3d cb 12 30 f4 bd a0 9c 9b
round  9:  63 2f af a2 eb 93 c7 20 9f 92 ab cb a0 c0 30 2b
round 10:  54 77 6f 20 4f 6e 65 20 4e 69 6e 65 20 54 77 6f
final:     54 77 6f 20 4f 6e 65 20 4e 69 6e 65 20 54 77 6f
```

Cut and paste the input

```
input:     54 77 6f 20 4f 6e 65 20 4e 69 6e 65 20 54 77 6f
```

We get the same data back that we started with.

