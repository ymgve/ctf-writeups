xenocryst - 420 points
======================

This challenge required you to reverse engineer a virtual machine that ran a
slightly modified [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck)
interpreter, then generate "shellcode" for this VM.

A quick top-down look at the binary in IDA shows this: The code allocates a
memory region of `0x300000` bytes, then does a LOT of initialization and setup
in that memory space. Being overwhelmed, I decided to skip static analysis
for now and go over to dynamic analysis.

I load the binary in GDB and see it reads a string from stdin, so I use the
`awatch` command to break the program whenever it reads or modifies the memory
where my input string resides. It first breaks on a strlen() call, then it
triggers a breakpoint inside the function `sub_1450`.

After a lot of single stepping I finally realize that this function is the
inner loop of a virtual machine, more specifically, a
[One Instruction Set Computer](https://en.wikipedia.org/wiki/One_instruction_set_computer)
VM. Each instruction is made up of five dwords:

```
 aaaa bbbb cccc dddd eeee
 src  dest size xtra nextip
```

In each instruction cycle, `size` bytes is copied from `src` to `dest`, and
the instruction pointer is forwarded to `nextip` (`xtra` contains an extra
dword that is generally unused, but can be used as an immediate constant
for the copy step). For the most part, all addresses are relative to the base
memory address of the VM. In the rest of this writeup, consider all given
addresses to be relative to this base address.

I dump the whole VM memory in GDB with `dump binary memory` and then start
looking through the result, reverse engineering what the VM program is
actually doing. One thing quickly stands out - the byte read from my input
string is used for lookup in a jump table at `0x00010000` in the VM memory,
where I notice an interesting pattern. Every value is `0x04`, except from
a few that correspond to the characters `#+,-.<>[]`, which I recognize
as the instruction set of Brainfuck, with the hash character added.

Testing out my theory, I give the string

```
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
```

as input, and in response I get

```
Hello World!
```

Theory confirmed.

Now it's time to dig deeper into the `#` character. Reversing more of the code,
I see that it reads the byte at the current position in Brainfuck memory, and
if it's either `0x80`, `0x83` or `0x84`, it reads some more parameters and
triggers system calls `exit(1)`, `read(3)` or `write(4)` respectively.

Being tired, I totally miss that you can actually specify the exact position
in BF memory to read from and write to, and spend a lot of time trying
to create BF programs that either move the BF instruction pointer or BF memory
pointer out of bounds. No such luck, as the bound checking is pretty robust on
those pointers.

After a night of sleep, I come back and finally see the code that reads the
offset parameter and adjusts it to the *real* x86 memory address. Now the
way to exploitation becomes clear:

- Do a system call in Brainfuck that writes some data from the VM memory
  (which contains the offset to x86 memory) to stdout
- Do another system call in Brainfuck that reads from stdin and overwrites
  part of the VM code with our own VM shellcode
- Trigger the shellcode, which will call `sys_execve` with our desired
  parameters

I'm interested in two dwords inside the VM code - the offset to the memory
block which is used to pass parameters from BF code to system calls, which
is positioned at `0x00012b30`, and the offset between the BF memory and
real x85 memory, which is stored at `0x00012b44`. The BF memory starts at
`0x00250f04`, and to shorten the BF code I will read 255 bytes from
`0x00012b04`, giving a relative offset of `0xffdc1c00`. I create a simple BF
program that puts this byte sequence in BF memory:

```
0x84 0x01 0xff 0x00 0x1c 0xdc 0xff
```

then uses `#` to trigger the `write` system call. 

I decide to overwrite the VM code that handles the `[` BF opcode, which is at
`0x000124bc`, and gives the relative offset of `0xffdc15b8`. As before, I put
this sequence into BF memory

```
0x83 0x00 0xff 0xb8 0x15 0xdc 0xff
```

and trigger the `read` system call, before finally executing `[` which runs
my shellcode.
  
After extracting the addresses I'm interested in, I create this customized VM
shellcode

```
000124c8 param+4  00000004 0000000b 000124d0    # system call 11 = sys_execve
000124dc param+8  00000004 arg1     000124e4    # arg1 = path to file to exec
000124f0 param+12 00000004 arg2     000124f8    # arg2 = pointer to argv list
00012504 param+16 00000004 00000000 0001250c    # no flags
00012518 param+0  00000001 ffffffff 00012520    # trigger the VM system call trap
00012520 00012520 00000000 00000000 00012520    # endless loop
arg1     00000000                               # argv list
"/bin/sh\x00"
```

which is then given into the waiting `read` call.

Finally, I get shell access, and get the flag from /home/xenocryst/flag
which is `blaze{I was gonna solve P vs NP but then I got high}`