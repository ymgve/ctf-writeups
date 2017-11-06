# Luaky - Crypto - 257 points - 29 teams solved

> Are you luaky enough?
>
> nc 13.113.99.240 50216
> 
> [luaky-b96e16b023d07964125fa8a401b62504.elf](./luaky-b96e16b023d07964125fa8a401b62504.elf)

# Very Luaky - Crypto - 342 points - 9 teams solved

> You need to be VERY LUAKY :)
>
> nc 13.113.99.240 50216
> 
> [luaky-b96e16b023d07964125fa8a401b62504.elf](./luaky-b96e16b023d07964125fa8a401b62504.elf)

In these challenges you must create a Rock-Paper-Scissors bot written in [Lua](https://www.lua.org) that can beat the server. Each round is 100000 hands, and you have to win 90000 of them to get a win. There are three different players in the server, each using a different simple pseudorandom generator with `state` seeded from `/dev/urandom`:

* Slime, which uses `state = (state + 1) % 3; cpuhand = state`
* Alpaca, which uses `state = ((state + yourlasthand + 0x9E3779B9) % 0x100000000); cpuhand = state % 3`
* Nozomi, which uses `state = ((state * 48271) % 0x7fffffff); cpuhand = state % 3`
 
You fight Slime for 1 round, then Alpaca and Nozomi for up to 10 rounds each, or till you lose, whichever comes first. To get the first flag you have to win 10 rounds against either Alpaca or Nozomi. To get the second flag, you have to beat 100 rounds where the bot is picked randomly for each round.

Your Lua script only requires one function, `play()`, which gives the CPU's last hand as input and expects your hand (0, 1 or 2) as output. There were no obvious security holes in the Lua jail (`os` and `io` libraries were not loaded), but you have access to `print` which greatly helps with debugging. In addition there is a time limit of 1 second for each round. (Someone told me post-contest that there is no time limit during the initial script load, so you could have used that time for computation instead)

Beating Slime is the easiest - just return the last hand the CPU did, and you win every time.

Beating Alpaca is a bit harder. Disregarding the `yourlasthand` for now since we control its content, we observe that `0x9E3779B9 % 3 == 0`. This means that if `state < (0x100000000 - 0x9E3779B9)`, then the next CPU hand will be the same as the last CPU hand. On the other hand, if `state >= (0x100000000 - 0x9E3779B9)` it will be changed by the modulus operation, and since `0x100000000 % 3 == 1` it means the next CPU hand will be predictably different from the last one. So by observing two previous CPU states you can narrow down which range `state` was in. We use two variables, `alp_low` and `alp_high`, that bound the predicted range of the CPU state. After a few rounds, this bound gets accurate enough that you can predict most of the CPU hands and therefore can easily beat it.

Beating Nozomi is the hardest. We spent quite some time trying to see if there's some mathematical way to use CPU hands to leak info about the state and rebuild it based on that, but didn't find any solution. After a while we started focusing on precomputation - we start with `state = 1` then generate a string consisting of the next 50 CPU hands after that state, then store it along with the next state in a lookup table. We generate 250000 such strings, spaced 9000 states apart. This is easy to do since the generator is basically a [cyclic group](https://en.wikipedia.org/wiki/Cyclic_group) - in Python, we can do `pow(48271, 9000, 0x7fffffff) = 1467418072` and then in Lua `state * 1467418072 % 0x7fffffff` is the same as skipping 9000 states ahead.

However, generating these strings takes quite a bit of time. We decided to spread the generation out over the rounds where we play against the other two bots. With the table ready, we can beat Nozomi. We take the last 50 CPU hands and see if it's in the table - if it is, we instantly know the next state from the lookup. Due to the way our table is constructed, we are guaranteed to find a lookup within the 9050 first hands, which gives us plenty of hands to win the round.

We got the first flag, and it is `hitcon{Hey Lu4ky AI, I am Alpaca... MEH!}`

For the second flag, we don't know which bot we're playing against in each round. So we use the first 50 hands to identify it - Slime is easy because it always changes hands predictably each round, and Alpaca is also easy since if you always pick 0 as your hand, it will either use the same hand as the last round or `(last + 2) % 3`, but never the remaining hand. If neither of those patterns fit, we know we're fighting Nozomi.

After 100 rounds we get the second flag - `hitcon{Got AC by r4nd() % 3! Nozomi p0wer chuunyuuuuu~ <3}`