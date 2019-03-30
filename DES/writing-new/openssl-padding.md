I struggled at first to make this work.  One key was discovery of a source for the flags, including ``-nopad``.

I found that part of the answer on StackOverflow [here](http://crypto.stackexchange.com/questions/12621/why-does-openssl-append-extra-bytes-when-encrypting-with-aes-128-ecb) with this quote

> padding is always applied. So, in the case of a full input block, another full block of ``0x10`` bytes will be added as padding, which means you'll have two blocks of output (which is what you see above).

As you can see in the man page above there is a ``-nopad`` flag:

> The -nopad option for openssl enc disables padding (but it will throw an error if your input isn't a multiple of the block size):


So even though our plaintext was exactly 8 bytes, openssl adds an extra block of 8 bytes to the input.


```bash
> openssl des-ecb -e -nopad -K "0E329232EA6D0D73" -in m87.bin | xxd -p
0000000000000000
>
```

A small contradiction to the StackOverflow answer above, from what I read before (about **PKSC#7**) [here](https://en.wikipedia.org/wiki/Padding_cryptography), the pad should be constructed from the byte whose value is equal to the number of bytes needed: '\x08' * 8.  

Try it.

```bash
> printf "\x87\x87\x87\x87\x87\x87\x87\x87\x08\x08\x08\x08\x08\x08\x08\x08" > m87p.bin
> openssl des-ecb -e -nopad -K "0E329232EA6D0D73" -in m87p.bin | xxd -p
0000000000000000a913f4cb0bd30f97
>
```

When we do ``-nopad`` but manually add our own padding according to **PKCS7**, the extra bytes we get match the bytes we got at first: ``a913f4cb0bd30f97``. 

It looks good.  We conclude that openssl just padded our input with ``\x08`` * 8.

And it's not just that openssl thinks the message should be at least 16 bytes, if we add our pad and then do

```bash
> printf "\x87\x87\x87\x87\x87\x87\x87\x87\x08\x08\x08\x08\x08\x08\x08\x08" > out.bin
> openssl des-ecb -e -K "0E329232EA6D0D73" -in out.bin -out enc.bin
> hexdump enc.bin
0000000 00 00 00 00 00 00 00 00 a9 13 f4 cb 0b d3 0f 97
0000010 a9 13 f4 cb 0b d3 0f 97                        
0000018
>
```

It pads out to 24 with another 8 bytes.  Notice the ciphertext repeats!

Apparently, the key material is re-used. A block ``\x08\x08\x08\x08\x08\x08\x08\x08`` gives ``a9 13 f4 cb 0b d3 0f 97`` repeatedly with this key.
