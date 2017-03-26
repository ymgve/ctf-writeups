# Casino - Crypto - 250 points

> Take your chances in our the most honest VolgaCTF Quals Grand Casino!
> casino_server.py
> casino.quals.2017.volgactf.ru:8788

This is a "guess the number" game which uses a [Linear-feedback shift register](https://en.wikipedia.org/wiki/Linear-feedback_shift_register) as its random number generator. Such random number generators can be attacked/solved with the [Berlekamp-Massey algorithm](https://en.wikipedia.org/wiki/Berlekamp%E2%80%93Massey_algorithm) - if you got got 2N bits of RNG output, where N is the degree of the LFSR polynomial. Since each guess gives us 6 bits and we have 20 wrong guesses before we run out of money, that gives us at least 120 bits to work with. N is randomly pucked by the server at connect - between 24 and 64, so most of the time, we have enough bits to work with.

To make things a bit harder for us, the server generates numbers mod 42 - which means that for most numbers, we have two choices for what the original number was. The solution to this is simple - just recursively generate all possible original sequences of bits - worst case 2**20 ~= 1 million different sequences - then use the Berlekamp-Massey algorithm on each of them.

To make sure we've found the right sequence, we tweak this slightly - we only use the first 17 guesses, with the remaining guesses used to verify if we found the right RNG. This means that our solver will fail if the server has picked a value for N larger than 51, but the odds are still in our favour.

After two runs, the solver found the flag - `VolgaCTF{G@mbling_is_fun_but_rarely_a_pr0f1t}`
