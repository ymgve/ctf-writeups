# Paillier Oracle - Cryptography - 267 points - 29 teams solved

> Paillier Cryptosystem is Hard, isn't it?
>
> nc oracle.tasks.ctf.codeblue.jp 7485
>
> [problem.py](./problem.py-0fcaaab8cb9e285aacc3e589202272b8440cef7bd20f734875239a01e3ceeee0)

This challenge implements the [Paillier cryptosystem](https://en.wikipedia.org/wiki/Paillier_cryptosystem) - we are given a public key, the encrypted flag, and an oracle which decrypts with the corresponding private key any ciphertext we give it, then show us the least significant bit.

Paillier is additive homomorphich, which means that if you multiply two ciphertexts, then decrypt the result, the result will be the sum of the two plaintexts. Basically, `ct1 = encrypt(pt1, pubkey)`, `ct2 = encrypt(pt2, pubkey)`, `decrypt(ct1 * ct2 mod n**2, privkey) = pt1 + pt2 mod n`. This also means that `ct = encrypt(pt, pubkey)`, `decrypt(ct ** x mod n**2) = pt1 * x mod n`

Due to the homomorphism, we can calculate `ct * ct mod n**2`, and the underlying plaintext will be `pt + pt mod n`. As long as `pt * 2 < n` the result should always be even. Since the flag is not padded before encryption, `pt` has fewer bits than `n` and is much smaller. As a result, `oracle(ct * ct mod n**2)` should always return the bit * `0`.

Now if we do `oracle(ct ** (1 << i) mod n**2)`, we should continue getting `0` as results since the underlying plaintext becomes `ptshift = pt << i`. We continue getting `0` as `i` increases until finally `ptshift > n`. Now this means one of two things - either `numbits(ptshift) = numbits(n) + 1` or `numbits(ptshift) = numbits(n)`.

To distinguish between these two cases, we attempt to remove the most significant bit of `pt`. The value `mask = 1 << (numbits(n) - i)` corresponds to the potential MSB, and we want to do `[pt - mask = pt + n - mask] mod n`. We again use the homomorphism property, and compute `tempval = ct * encrypt(n - mask, pubkey) mod n**2`. If the upper bit was actually set, it is now cleared, but if not we are left with a value close to `n` due to the subtraction going below zero. To distinguish between these two cases, we use `oracle(tempval ** 2 mod n**2)`. If the result is `0` we cleared the upper bit, if the result is `1` we generated an underflow.

In the former case, we simply append `1` to our known flag bits, and use `tempval` as our new ciphertext. In the latter case, we instead generate `mask = 1 << (numbits(n) - i - 1)` and use that to remove the actual MSB which is to the right of the one we first attempted, and which is guaranteed to be present. One caveat is that this bit is removed "out of order" so our code have to remember this.

By repeatedly doing the full process as we iterate over `i`, we get the plaintext bit by bit, and after a while we have the full flag, `CBCTF{0a5b6a97044b3bccff21200292592979d5dc9ac6}`
