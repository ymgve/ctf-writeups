# Corroded Alien Artifact - Reversing - 500 points

> Looks like ancient civilizations aren't the only ones to leave us a message, some friendly alien civilization also said hi! The bad news is the message was too corroded to decipher. The good news is we were able to recover a tool to verify its correctness, the not so good news is driew si ygolonhcet neila. Can you help us recover the message? 
> [Download](./ctf_alien_cpu-07fbf219680f2676964018bbcb008968.zip)

Binary is a 64bit Windows executable (Don't see those too often in CTFs). We load it up in [x64dbg](https://x64dbg.com) and run it, and soon see that it throws an `EXCEPTION_ILLEGAL_INSTRUCTION` exception. We look at where the exception happened, and notice that just before the illegal instruction, it sets up an exception handler:

![Handler setup](./images/handler_setup.png)

On a `0F B9` illegal instruction, the handler sets RIP to `0x0000000140002480`, pushes a return address on stack, then enables single step mode. On a `0F 0B` illegal instruction, the return address is popped and single step mode is disabled.

In addition, on a `STATUS_SINGLE_STEP` exception, the code either leaves RIP alone if the last nibble of RIP is 0, or sets the last nibble to 0 then subtracts 0x10 from RIP. Basically, it executes instructions offset at 0x10 bytes from each other in reverse sequence (unless a jump/call just occured).

Trying to understand the jumbled instructions is way too hard, so we pull out the [Capstone](http://www.capstone-engine.org/) disassembler and write a small Python script to disassemble the flag checker function.

(The challenge author has uploaded the source code for the challenge, so take a look at the flag checker code [here](https://github.com/athre0z/ctf-alien-cpu/blob/master/src/flag-logic.rs).)

Static analysis can give you some of the characters of the flag easily, but the most important part of the logic is the checksum part - since we know the flag is alphanumeric, we can brute force each 6-character sequence until we find something that looks like part of a flag.

After some analysis and brute force we get the final flag: `FLAG{ysrever_mees_slliks_ruoy}`
