# Irene Adler - Exploitation - 148 points - 27 solvers

> Known professionally as "The Woman". She actually proved that [Love](./irene_adler_aea6a22a4a2f80fec728cf3519aa4d9798620cdc) is the most dangerous vulnerability, Sherlock exploited her easily by "I am SHER-Locked." But can she finally exploit Sherlock?
>
> `nc 146.185.132.36 31337`

The binary is a text game coded partially in [Lua](https://www.lua.org/) that is a simple variant of the [Elite](https://en.wikipedia.org/wiki/Elite_(video_game)) space trading game. You fly between planets, buying and selling goods, trying to earn enough money to get bigger and better ships.

In this challenge, the goal is to either get the `flagship` space ship, which got the flag in its inventory, or find some other way to obtain the `flag` trade item.

I don't have much experience with Lua internals, so my approach was to try finding some logic bug in the game code. After a while, I found out that the `Soylent` trade item decays in flight depending on the distance traveled. The decay amount is capped at 100%, but there is another feature where you get stranded and need to be rescued by other traders if you run out of fuel, and this makes your Soylent inventory decay by _another_ 10%. So it's possible to get the decay to 110% by traveling between the most distant star systems with low fuel, which causes the amount of Soylent you're carrying to underflow.

Then it's just a matter of selling Soylent until you have enough money to buy the flagship, and listing its inventory gives you the flag `ASIS{gj_Y0U_oWn3d_ouR_LU4_PWN_task_!}`
