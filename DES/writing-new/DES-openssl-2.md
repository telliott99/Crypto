#### Example from the DES ECB tutorial.

There is another example in the [reference](http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm).  The message is

- **Your lips are smoother than vaseline**

I use Python 3 to get the message on disk.

```bash
>>> s =  "Your lips are smoother than vaseline"
>>> L = [ord(c) for c in s]
>>> with open('lips-msg.bin', 'wb') as fh:
...     fh.write(bytearray(L))
...     fh.write(b'\x0d\x0a\x00\x00')
... 
36
4
>>>
```

We added the newline from Windows ``0d0a`` and also two more zero bytes ``0000``.  The reason is that now we have a total of 36 + 4 = 40 bytes, which is a multiple of 8.  The newlines and the null bytes together are our padding.


```bash
> hexdump -C lips-msg.bin 
00000000  59 6f 75 72 20 6c 69 70  73 20 61 72 65 20 73 6d  |Your lips are sm|
00000010  6f 6f 74 68 65 72 20 74  68 61 6e 20 76 61 73 65  |oother than vase|
00000020  6c 69 6e 65 0d 0a 00 00                           |line....|
00000028
>
```

We encrypt it as before:

```bash
> openssl des-ecb -nopad -e -K "0E329232EA6D0D73" -in lips-msg.bin -out enc.bin
> hexdump enc.bin
0000000 c0 99 9f dd e3 78 d7 ed 72 7d a0 0b ca 5a 84 ee
0000010 47 f2 69 a4 d6 43 81 90 d9 d5 2f 78 f5 35 84 99
0000020 82 8a c9 b4 53 e0 e6 53                        
0000028
> 
```

This matches what they have in the article.

<hr>

#### Key size

```bash
> openssl des-ecb -e -nopad -K "YELLOW SUBMARINE" -in m87.bin | xxd -p
non-hex digit
invalid hex key value
> openssl des-ecb -e -nopad -K "0E329232EA6D0D73" -in m87.bin | xxd -p
0000000000000000
> openssl des-ecb -e -nopad -K "0E329232EA6D0D730E329232EA6D0D73" -in m87.bin | xxd -p
0000000000000000
> openssl des-ecb -e -nopad -K "0E329232EA6D0D73FFFFFFFFFFFFFFFF" -in m87.bin | xxd -p
0000000000000000
>
```

It'll take a bigger key as long as it's hex, but it won't use it all.
