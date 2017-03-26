# Transformer - Reversing - 400 points

> We've got a file that was processed with a binary called transformer. We really need the contents of this file. Can you help?
> ciphertext.zip.enc
> transformer

This is a binary written in Rust that encrypts a file, and we have to find a way to reverse the decryption to get the flag from the attached encrypted file.

First thing to do is load the binary into IDA. Rust is still compiled to x86/x64, so we can use all our standard tools. When loaded, we see that there are tons of symbols in the file - not sure if this is a side effect of Rust, or just the challenge creators being generous. After a few minutes we discover a class of functions named `transformer::rc5`, which hints that this might be an implementation of the [RC5 encryption algorithm](https://en.wikipedia.org/wiki/RC5).

To get a better understanding of it, we created a dummy plaintext file, fired up GDB and set breakpoints at the `transformer::rc5::Rc5::new::h30d6eb4c1bfeb265` and `transformer::rc5::Rc5::encrypt_block::hc307a8b30c5c81e1` functions. Inspecting the parameters we discovered that it initializes two key schedules with two sets of keys: `0xa89193a0, 0x5c3987ca` and `0x32af5f86, 0x74719560`. The parameters of the `encrypt_block` function showed that the former key was used to encrypt a randomly picked dword plus an increasing number. The latter key was used to encrypt bytes from our input file. To see how these pieces interact, we examined the function that called `encrypt_block` and noticed that both values were XORed together. This looked like a custom version of the [CTR encryption mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Counter_.28CTR.29). We deleted all breakpoints, let the program run till it terminated, and then inspected the resulting encrypted file. We saw that the first four bytes of the file were the same as the random dword, and that the data after that matched the XORed data we observed. Surprisingly enough, we also saw that some data, at regular intervals, weren't encrypted at all. Never found out if this was a bug or intended behavior.

We then wrote our own implementation of RC5 in Python and used it to decrypt the `ciphertext.zip.enc` file. Inside was a text file, which contained the flag - `VolgaCTF{Wh1te_b0x_crypto_i$_not_crYpto}`
