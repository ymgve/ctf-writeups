# Vermatrix Supreme - Cryptography - 100 points

> Working in IT for a campaign is rough; especially when your candidate uses his password as the IV for your campaign's proprietary encryption scheme, then subsequently forgets it. See if you can get it back for him. The only hard part is, he changes it whenever he feels like it.
>
> nc vermatrix.pwn.democrat 4201
>
> handout
>
> author's irc nick: negasora

Need to reverse the matrix functions and recover the original IV to get the flag. `fixmatrix()` is simpler than it looks - it's just XOR between the matrixes and therefore easily reversible. One stumbling block is that the given source code is 'lying' - it looks like it is supposed to be a 9-character string, but in reality is a list of 9 integers between 0 and ~1200. Sending back the correct IV gives us the flag, `flag{IV_wh4t_y0u_DiD_Th3r3}`
