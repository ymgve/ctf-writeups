# Boxes of Ballots - Cryptography - 200 points

> Privjet Komrade!
>
> While doing observing of Amerikanski's voting infrascture we find interesting box. We send operative to investigate. He return with partial input like showing below. He say box very buggy but return encrypted data sometimes. Figure out what box is do; maybe we finding embarass material to include in next week bitcoin auction, yes?
>
> `ebug": true, "data": "BBBBBBBBBBBBBBBB", "op": "enc"}`
> 
> nc boxesofballots.pwn.republican 9001
> 
> author's irc nick: Unix-Dude

Can send something like `{"debug": true, "data": "BBBBBBBBBBBBBBBB", "op": "enc", "key": "XXXXXXXXXXXXXXXX"}` and get
encrypted data back. Decryption operation is not available - messing around with parameters returns stack traces which
reveal parts of the serverside code. The server is doing AES128 in [CBC mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Block_Chaining_.28CBC.29), with the input
plaintext padded to a multiple of 16 with space characters. IV is initially unknown, but since we control plaintext and
encryption key, we can do the decryption locally and find the IV by reversing the CBC function.

If `debug` is set to `false`, the server switches modes - instead of our key, it uses the same IV, but a secret server-side
key, and the flag is appended to our plaintext before padding. To find the flag, we align the plaintext so one byte of the
flag is in its own block, then take the ciphertext of that block and try to match it by manipulating the content of the first block. Once one byte is known, we can bruteforce the next byte and so on. Finally, the whole flag is revealed - `flag{Source_iz_4_noobs}`
