**command**:

```
echo -ne '\x87\x87\x87\x87' > m87.bin
echo -ne '\x87\x87\x87\x87' >> m87.bin
hexdump -C m87.bin
```

**output``:

```
00000000  87 87 87 87 87 87 87 87                           |........|
00000008
>
```

The ``-n`` flag means no newline, and if we don't have the ``-e`` flag, ``echo`` writes the characters ``\x87`` etc. to disk (i.e. the four bytes ``5c 78 38 37`` repeated 8 times).