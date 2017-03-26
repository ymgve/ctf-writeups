# Curved - Crypto - 200 points

> This server is willing to perform several commands and cat is among them. However, to execute cat flag we need to provide the signature. We only have signatures for exit and leave commands which is cruelly ironic. Can you help us to get the flag?
> curved_server.py
> exit.sig
> key.public
> leave.sig
> curved.quals.2017.volgactf.ru:8786

The server script executes shell commands, but only those signed with a proper [ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm) signature. We don't have the private key, so we can't sign our own commands.

If we open both .sig files, we quickly notice that the first value is the same in both signatures. This value is the `r` value, which is derived from the private `k` value, which should be an **unique**, cryptographically secure generated random number. Re-using this value is a huge security flaw, which is somewhat famous, because that was the mistake [Sony did with the Playstation 3](https://arstechnica.com/gaming/2010/12/ps3-hacked-through-poor-implementation-of-cryptography/), and it allows the full recovery of the private key.

After some quick googling we found [code examples for recovering the private key](http://bitcoin.stackexchange.com/questions/35848/recovering-private-key-when-someone-uses-the-same-k-twice-in-ecdsa-signatures) on StackExchange. After using this code we can then sign our own shell commands, and using `cat flag` gives us the flag `VolgaCTF{N0nce_1s_me@nt_to_be_used_0n1y_Once}`
