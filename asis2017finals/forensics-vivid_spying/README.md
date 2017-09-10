# Vivid Spying - Forensics/Network - 131 points - 32 solvers

> We have captured the spy [traffic](./traffic_f02965261bd4de3e9a10fced162c27fe5c2c5b19) by our agents, hurry up and find the flag.

We open the attached file in Wireshark and find it's a series of DNS queries and responses about suspicious domain names, starting with `00101011111010110111101100101010010010110010101000001.asisctf.com` and ending with `1110.000011101100101011111010110111101100101010010010110010101000001.asisctf.com`. We quickly find that if you reverse the string and convert the bits to ASCII you get something that looks like a partial flag `ASIS{_Sp`. But how to get the rest?

After some experimenting we find that if we query the DNS server at `95.85.26.168` with a domain formatted like the suspicious ones we either get `NXDOMAIN` (for example for `0.asisctf.com`), or `NOERROR` (for example for `1.asisctf.com`). We can then continue with trying `01.asisctf.com` and since we get `NOERROR` for that one too, we know the bit we added at the left is correct. We write a script that extends in this way to find the full flag, adding periods when needed (because domain fragments can't be longer than 63 bytes).

After a short while we get the full flag, `ASIS{_Spying_with_DNS_!}`
