# Common Modulus 1 - Cryptography - 98 points - 162 teams solved

> We made RSA Encryption Scheme/Tester. Can you break it?
>
> [Common_Modulus_1.zip](./Common_Modulus_1.zip-37882dbd7dd05381bbf72a11fbbdb3f23def0e4981bc9ffcd399e4c138549fc8)

# Common Modulus 2 - Cryptography - 133 points - 104 teams solved

> The previous one is very easy. so is this also easy?
>
> [Common_Modulus_2.zip](./Common_Modulus_2.zip-24d74ea8d1b7bc154d30bb667f6f13ef24a9fe260a7741caab427421d1070c98)

# Common Modulus 3 - Cryptography - 210 points - 48 teams solved

> try harder!
>
> [Common_Modulus_3.zip](./Common_Modulus_3.zip-275005199fd0ecbec4183fd7e1b421f65c7bb982ffba65a12a4089e263899152)

These challenges are three variations of the same problem, where a plaintext is RSA encrypted twice, with public keys `(e1, n)` and `(e2, n)` where `n` is the same in both keys but `e1 != e2`. We are given a file with both public keys and the two ciphertexts `ct1` and `ct2`.

At first I totally missed that `e1` and `e2` was explicitly given in the files, so I wrote a script to brute force find the private keys by generating `ct1 ** x mod n` and `ct2 ** y mod n` until I found a match. This works because `(m ** e1) ** x = m ** (e1 * x) = m ** (e2 * y) mod n` when `e1 = y` and `e2 = x`. Since each `e1` and `e2` are generated from a random number below `2 ** 20` this just takes a few minutes.

With the two public keys fully known, the solution is as described [in this Stackexchange post](https://crypto.stackexchange.com/questions/1614/rsa-cracking-the-same-message-is-sent-to-two-different-people-problem) - you take the extended GCD for `e1` and `e2` to find two values where `e1 * s + e2 * t = 1` which then can be extended to `[(ct1 ** s) * (ct2 ** t) = (m ** (e1 * s)) * (m ** (e2 * t)) = m ** (e1 * s + e2 * t) = m ** 1 = m] mod n`. The only issue is that either `s` or `t` is negative, so you have to use modular multiplicative inverse to calculate a negative power. After this, we get `m`, convert it to bytes, and get the first flag `CBCTF{6ac2afd2fc108894db8ab21d1e30d3f3}`

In the second problem, `e1` and `e2` is generated with `e = 3 * get_random_prime(20)`, so they have a common factor. We simply divide both of them by 3, and the above alorithm still works. The only problem is that we are left with the result `m ** 3`. Since the number of bits in `m` is assumed to be less than one third of the size of `n`, we can simply find the cube root of the result, and get the proper `m`. The second flag is `CBCTF{d65718235c137a94264f16d3a51fefa1}`.

In the third problem, the common factor is now `17`, but more importantly, the flag is left aligned with zero bytes until the plaintext is 8192 bits in length. In practice, this means that `mp = m ** (1 << (x*8))`, and the value we get when repeating the algorithm from the previous problems give us `mp ** 17`. Our solution then becomes to generate modular multiplicative inverses for all `1 << (x*8) mod n`, then try all of them. One of them will leave us with `m ** 17` as the result, which we then can take the 17th root of to get the original `m`, and the flag which is `CBCTF{b5c96e00cb90d11ec6eccdc58ef0272d}`.
