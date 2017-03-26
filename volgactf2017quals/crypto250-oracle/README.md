# Oracle - Crypto - 250 points

> An encrypting and decrypting oracle was found at oracle.quals.2017.volgactf.ru:8789. We managed to get it's script. No flag can be seen...
> UPD
> We searched thoroughly for several hours and found some ciphertext:
> 
> b'\xab\xb9\xe8\x22\x05\xad\xef\xa2\xfa\xdf\x37\xe5\x90\xfe\x2f\x2b\x5b\x9f\xef\x4d\xb9\x11\x88\xfb\x58\x18\xf5\xa6\x63\xa7\x10\xf3'
> Will it help?
> cryptoclient.py
> cryptoracle.py

We are given those 32 bytes in the challenge description, and it seems logical that they contain the flag in encrypted form. Considering the name of the challenge, we assume the challenge is to make the server decrypt and reveal information about the plaintext for us, so we don't need to know the key - an *Oracle* attack. After some study of the server code it becomes clear that we need to use a [Padding Oracle attack](https://en.wikipedia.org/wiki/Padding_oracle_attack).

Using this attack, we manage to reveal that the first block contains `VolgaCTF{B3w4r3_` but the second block is `\x9b\xdf\xb7r1\xc9\x8b\x93\x94\xb8J\xe0\x95\xfb*.` - did something go wrong?

We then realize that the flag is encrypted in [CBC mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Block_Chaining_.28CBC.29) with no IV, so we simply XOR the the first ciphertext block with the second plaintext block we got, and we finally have the full flag after removing padding - `VolgaCTF{B3w4r3_0f_P4dd1ng}`
