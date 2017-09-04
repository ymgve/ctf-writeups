# Backpacker's Problem - Programming - 177 points - 20 solvers

> Enjoy PPC!
>
> `$ nc backpacker.chal.ctf.westerns.tokyo 39581`
>
> [backpacker-server.7z](./backpacker-server.7z-cac1702a29b9c29af680939d8b40e62325046c9d47faf5f7fdb322fb75c9f728)

In this challenge we have to solve 20 [Subset sum](https://en.wikipedia.org/wiki/Subset_sum_problem) problems, in increasing difficulty from 10 items to 200 items. Subset sum is a variant of the [Knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem), which is where the challenge gets it name. As this problem is [NP-Complete](https://en.wikipedia.org/wiki/NP-completeness), the processing power required to solve a problem increases exponentially with the size of the problem.

In this challenge, pure brute force can only solve the first two problems of size 10 and 20. Using [meet-in-the-middle](http://www.geeksforgeeks.org/meet-in-the-middle/) we can solve the four first problems, up to size 40. More advanced techniques can solve up to problem five and six (Someone mentioned using [LLL](http://www.math.ucsd.edu/~crypto/Projects/JenniferBakker/Math187/#Anchor-Th-54278) but I haven't looked into that), but it's clear that it's impossible to solve this challenge if we approach it as a pure algorithmic problem.

However, we are given the server source code, which is normally a good indication that we have to find a flaw in the actual algorithm implementation. The most obvious issue with the code is that the random numbers are generated via the [Mersenne Twister](https://en.wikipedia.org/wiki/Mersenne_Twister) PRNG.

Problem sets are generated this way:
* set `n = 10x` where `x` is the problem set number
* generate `n/2 - 1` PRNG 'solution' integers, each 100 bits in length
* sum them all up, then add the negative of this as an extra integer, ensuring that the first half sums to zero
* generate `n/2` additional PRNG integers
* sort the numbers, which shuffles the 'solution' integers in with the non-solution ones
 
Because the integers are 100 bits long, we can recover three out of every five PRNG outputs. This is not enough to recover the full PRNG state and we can't use attacks like the [Mersenne Twister Predictor](https://github.com/kmyk/mersenne-twister-predictor). We spent some time trying to look for flaws in how the problem sets are generated, but didn't find any exploitable issues.

Let's look at the [Python implementation](https://en.wikipedia.org/wiki/Mersenne_Twister#Python_implementation) of the Mersenne Twister.

    def __init__(self, seed):
        # Initialize the index to 0
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = seed  # Initialize the initial state to the seed
        for i in range(1, 624):
            self.mt[i] = _int32(1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)
                
Initially, the array `mt` is filled with 624 32bit integers generated from a 32bit seed. This process is trivial to invert - if you know any `mt[i]` it is possible to calculate backwards and find the original `seed`. However, before the array is used (and every time the array has been "used up") a `twist()` function is called to further diffuse the randomness:

    def twist(self):
        for i in range(624):
            # Get the most significant bit and add it to the less significant
            # bits of the next number
            y = _int32((self.mt[i] & 0x80000000) +
                       (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
                
        self.index = 0
        
If we can recover any of the `mt` array values before the twist was done, we can recover the seed. At first glance this seems hard since to recover either the original `mt[i+1]` or `mt[i+397]` you need the original other one, and they are overwritten later in the loop. Except...it loops around. For example, the new `mt[227]` will be generated from the values of the *new* `mt[0]` in combination with the *old* `mt[228]` If we know the new `mt[0]` and `mt[227]`, we can reverse the twist function and recover the original `mt[228]`, which then can be used to recover the PRNG seed. (We ignore the old `mt[227]` because it only contributes a single bit and is trivially bruteforceable).

If we manage to solve the first two problem sets and reach the third one, the server has used `5 * (10 + 20 + 30) = 300` PRNG values. The 0th and 227th of these values are the ones we need, and because of the way the 100 bit integers are generated, we know that the 0th and 227th will be among the PRNG values we are able to extract.

The only issue remaining is that we don't know exactly which of the extracted values are the 0th and 227th due to the sorting of the problem sets, but trying all pairs of values is easily bruteforceable.

Our core code to find candidate seeds:

    def get_seeds(m0, m227):
        seeds = []
        y_even = (m227 ^ m0) << 1
        y_odd = (((m227 ^ m0 ^ 0x9908b0df) << 1) & 0xffffffff) | 1
        for y in (y_even, y_odd):
            for oldm227_upperbit in (0, 0x80000000):
                for oldm228_upperbit in (0, 0x80000000):
                    n = y ^ oldm227_upperbit ^ oldm228_upperbit
                    for i in xrange(228, 0, -1):
                        n = ((n - i) * 2520285293) & 0xffffffff
                        n = n ^ (n >> 30)
                        
                    seeds.append(n)
        return seeds


There are eight possible candidate seeds, depending on whether `y` originally was odd or even, and whether the upper bits of the original `m[227]` and original `m[228]` were set. We brute force over these possible candidates for all recovered PRNG values, then initialize the MT with each of the seeds in order, generating a few PRNG values for each seed to see if we get a match.

When we get a match and know the seed, we can just follow the same procedure as the server and generate the same problem sets as the server does. Due to the way they are generated, we instantly know the correct solution, and can simply send it to the server. After the 20th challenge is done, we got the flag `TWCTF{CPP_have_some_traps}`.
