# ABC - Reverseing - 73 points - 70 solvers

> Start [Reverse](./abc_b96c97d1229d3275cc9ee51f6b2b3d7c5be36446)

Loaded the binary up in IDA and decompiled - program seems simple enough, it expects a 12 character string as the password, then applies the function at `0x4024DF` to the four first, middle six, and four last characters.

What does the `0x4024DF` function do? It seems to be some form of cryptographic function judging from the tons of XOR and rotations being done. One trick when examining such a function is to simply Google any suspicious "magic" numbers. And sure enough, Google shows that the number `0xC3D2E1F0` is used in the [SHA-1](https://en.wikipedia.org/wiki/SHA-1) hash function. The hash of the middle six characters is also compared to a 20-byte string, which matches the hash length of SHA-1.

The string `69fc8b9b1cdfe47e6b51a6804fc1dbddba1ea1d9` is the hash of the middle six characters. We assume that they all are printable, so let's fire up [Hashcat](https://hashcat.net/hashcat/):

    hashcat64 -m 100 -a 3 69fc8b9b1cdfe47e6b51a6804fc1dbddba1ea1d9 ?a?a?a?a?a?a
    
After a few minutes, the hash is cracked: `9:-*)b`

The hashes of the first and last four characters aren't compared to a stored hash, however - they are compared to themselves. Basically, `hex(sha1("0123")) == "0123...................................."`. We write a quick brute force program that finds strings that match themselves, and it finds there are only two such strings: `57d9` and `b53a`. Since the four-character sections overlaps with the six-character one, we know which one will fit where, and get the final password: `57d9:-*)b53a`. Putting this into the program gives the final flag (Which is just the SHA-1 hash of the password): `ASIS{477408a4d4ad68aa7abdfd2be0e4717154497c42}`