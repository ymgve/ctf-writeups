# Time Is - Exploitation - 150 points

> Check out an extremelly useful utility at time-is.quals.2017.volgactf.ru:45678
> time_is

This binary reads in a space separated list of time zones, then converts the current time to them all. This is done in a loop, so we can do this repeatedly.

We did some quick observations:
* no errors on invalid time zones
* `__printf_chk()` is given user controlled input as the first parameter
* but `__printf_chk()` is also blocking some normal printf attacks like %123$p and %n
* no length checking of input buffer, but stack canary is present

We spent a short time trying to see if there was a flaw in the line splitting or time zone code, but realized this was unneccessary - `__printf_chk()` is still flawed enough to be exploitable. Even if parameter offsets like %123$p don't work, **tons** of parameters still work. So we just used %p%p%p%p%p%p%p%p%p%p%p... until we were at the desired offset. We first used this combined with %s and user speficied offsets to dump some of the resolved addresses from the GOT. We then used those addresses combined with [a libc database](https://github.com/niklasb/libc-database) to find the correct libc version used by the server, in this case `libc6_2.23-0ubuntu7_amd64.so`.

Next, we used the same %p%p%p%p%p%p%p%p%p%p%p%p%p%p... trick to print out the stack canary value and the return to `__libc_start_main` to locate the libc base address.

With the canary value known, we could smash the stack and overwrite the return from main() with a simple ROP chain that did `system("/bin/sh")`. Using the shell, we found the flag - `VolgaCTF{D0nt_u$e_printf_dont_use_C_dont_pr0gr@m}`
