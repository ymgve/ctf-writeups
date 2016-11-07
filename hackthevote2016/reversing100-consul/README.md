# Consul - Reversing - 100 points

>Bernie Sanders 2018
>
>consul
>
>author's irc nick: mxms

Program is total spaghetti and doesn't do anything useful on execution. But there is an area with strings that seem to be XORed with a constant byte in some functions, so let's just brute force until we find a flag.

A small script later, and we have the flag `flag{write_in_bernie!}`
