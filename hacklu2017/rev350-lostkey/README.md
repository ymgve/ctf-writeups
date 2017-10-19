# LostKey - Reversing - 350 points

> You know the area around your house at the edge of the world quite well. However, the world is big and its edge is long. To have a look at the other parts of the world's edge, you took one month off and planned a road trip. But you just can't seem to find your car key... Luckily you've left yourself some hints where you might find it, as this is not the first time you forgot where you've put it! 
> [Download](./LostKey-c98d722d57033d6463abd405a70d86aa.zip)

Binary is a 32bit ELF. It takes four arguments, then passes each argument to a separate thread in sequence. We first loaded it up in `gdb`, then used `set follow-fork-mode child` to ensure threads were debugged too. We set an `awatch` on the start of the first command line argument in the stack, then ran the program. We got a hit inside the first new thread, at address `0x0804A210`. After a bit of study we realized the program executes small code fragments via [ROP](https://en.wikipedia.org/wiki/Return-oriented_programming).

This first sequence of instructions reads the first four characters of `argv[1]` as an int, XORs with `0x466C7578` and checks if the answer equals `0x210D191E`. If true, it reads the next four characters, XORs with `0x78756C46` and checks if the answer equals `0x4B1D383D`. If both are true, it copies the argument into a buffer which is printed at the end of the program. Inverting the two XORs gives us the first part of the flag, `flag{Th3`.

We struggled a lot with trying to get the watchpoint on the second argument to trigger - not sure if it was our setup or `gdb` itself, but it seemed to lose track of breakpoints/watchpoints once the first thread returned. The solution became to set a breakpoint in the main thread right before thread creation, then only using `set follow-fork-mode child` and setting break/watchpoints right before we enter the thread we're interested in examining.

The second sequence of instructions iterates over each character in `argv[2]`, doing some bit manipulation then XORing with the next character in the sequence. The final result is then compared with the values set at offset `0x08049ADC` in the code. Again, this is easy enough to invert, and gives us our second part of the flag - `_key_1s_in_th3_secret_com`.

The third sequence seems to just call a hash function - the result from the function was `0b4e7a0e5fe84ad35fb5f95b9ceeac79` for our placeholder `argv[3]`, and a quick Google search says it's the [MD5](https://en.wikipedia.org/wiki/MD5) hash of `aaaaaa`. The code then checks if the hash equals `7b4d6ff46ac46c3f628acc930d937d81`, which gives no Google hits. But our sample hash shows it was only six characters, which is easily bruteforceable. So we pull out [Hashcat](https://hashcat.net/hashcat/), run `hashcat64.exe -m 0 -a 3 7b4d6ff46ac46c3f628acc930d937d81 ?a?a?a?a?a?a` and get the result `p4rtme`.

The fourth and final code sequence encrypts `argv[4]` with [TEA](https://en.wikipedia.org/wiki/Tiny_Encryption_Algorithm) - three blocks, so 24 bytes in total, then compares the result with the values set at `0x08049E03`, `0x08049F92` and `0x0804A121`. Our first attempts at decrypting these values failed, but then we realize the key used (fetched from `0x080EA39C`) is based on whether certain calls to `ptrace` succeeds and fails - a sneaky anti-debugger trick. With the correct key, we got the final part of the flag `nt_of_your_t00l_sh3d...}`.

When all pieces are put together, we get the final flag - `flag{Th3_key_1s_in_th3_secret_comp4rtment_of_your_t00l_sh3d...}`
