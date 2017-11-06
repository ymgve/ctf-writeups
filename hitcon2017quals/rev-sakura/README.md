# Sakura - Reversing - 218 points - 50 teams solved

> She accompanies me every night.
> 
> [sakura-fdb3c896d8a3029f40a38150b2e30a79](./sakura-fdb3c896d8a3029f40a38150b2e30a79)

This binary reads 400 bytes from stdin, runs a lot of verification tests on the input, then gives the flag as the SHA256 hash of the input. While the verification function is huge (and makes Hex-Rays choke a bit), it is pretty neatly structured. Each step adds up different digits from the input then verifies that the sum of those digits match.

Our [angr](http://angr.io/) skills are a bit rusty, and this seems like an ideal task to freshen up those skills. The thing that worked really well this time was the `avoid` parameter to `explore()` - the verification function doesn't return instantly on failure, it just clears a flag then continues executing the rest of the function - if we just told `angr` to reach the flag printing code, it would spend a lot of time analyzing dead paths. So we give it a list of addresses that instantly terminate an analysis branch if ever reached, cutting significantly down on the amount of work the analyzer has to do. We also hacked in some step-by-step debugging output by doing `explore()` in smaller chunks to see how well `angr` is doing, though there's probably some better way to do this.

After a few minutes, `angr` had found valid input, and we fed it into the program and got the flag in return - `hitcon{6c0d62189adfd27a12289890d5b89c0dc8098bc976ecc3f6d61ec0429cccae61}`
