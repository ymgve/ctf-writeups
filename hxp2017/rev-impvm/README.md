# impVM - Reversing - 400+100 points - 1 team solved

> Flavour text
> Our inside man in Company $x made us aware of a new DRM schem they are employing. By accident he was able to aquire the program they use to encode their data with (rev.cmp), unfortunately the decoding algorithm was out of his reach. Internal documents state, that they use a custom, highly secure, state of the art virtual machine (VM). Quickly thinking he punched a whole, with a round house kick, into the firewall to make the VM reachable from the internet. From promotional documents he also recoverd a second program, ‘BrainFuckInterpreter.cmp’. The name speeks for itself.
>
> Your goal
> write a program that does the inverse of rev.cmp
to initialize the challenge call #252. This overwrites the first 6 memory cells in global data.
to check the solution call #253
>
> Download:
> [fbfcddf7315613e511e9a8910fb5a028c5ea02ec398dec5ba1427a7deb73842c.tar.xz](./fbfcddf7315613e511e9a8910fb5a028c5ea02ec398dec5ba1427a7deb73842c.tar.xz)
>
> Connection:
> nc 35.205.206.137 8080

(Challenge author's reference code can now be found at https://github.com/leetonidas/impVM)

In this challenge we have to figure out the inner workings of the Virtual Machine from the short description and the two example programs. We can do `nc 35.205.206.137 8080 < BrainFuckInterpreter.cmp`, and we get the familiar ["99 bottles"](http://www.99-bottles-of-beer.net/) text in response. Studying the interpreter program in a hex editor, we see that it has a central header and six data sections. The last of these contain the actual Brainfuck "99 bottles" program. Each section contains a number at the start, but it doesn't match up with the section sizes.

We look at the non-Brainfuck sections alongside each other, and see some obvious patterns:

    000000000000011F 60180200201C0140315E00A0380280FF80280E00A07FFB802C0E00F7E0038020
    0000000000000025 C01403A1C02C0140703FAC0303600A03F801C0140300A04C01607007BF600B01
    0000000000000066 C0180200300C0140300A04C01607007BF600B0080700500CBB80280E00A03FE0
    000000000000006E C0180200300C0140300F980502600B03803DF902600B03803DFB005804038028
    000000000000002A C014070050160180280E00A0380280E00A03F600A05802817BE7B802C0E00F7E
    
The most obvious pattern is that we see `C01` a number of times in the data. But the distance between the first and second occurence in those lines is 11 characters - so 44 bits, which isn't divisible by 8! Maybe instructions don't fit neatly into bytes? As a test, we dump the data as bit strings and try to split them in various sizes. It seems like 11 bits fits pretty nicely, at least at the start.

    01100000000
    11000000000
    10000000000
    01000000001
    11000000000

But then after a while it goes "out of sync" - maybe the instruction size isn't fixed, but 11 bits per instruction seems like a good place to start. Revisiting the number at the start of each section - if we consider it the number of instructions instead, it almost fits with the section sizes, but not exactly.

Time to do some fuzzing - we replace the section of the `rev.cmp` program with random bytes and see if we get some results at all. After repeating this process for a while, we finally find a random byte string `7e2bf5b6a23daae62529...` that gives a "try harder next time" response from the server. This sounds like we somehow managed to call function number `253` as mentioned in the challenge description. We reduce the string until it doesn't work anymore, and find that `7e2bf5` is the smallest program that produces this message. We also reduce the instruction count in the program, and can reduce it to `2` with the message still showing up.

If we write this as 11-bit instructions it becomes `11000000000 01011111101 01`. The number `253` in binary is `11111101` so it matches the last part of the second instruction. From this we are reasonably sure the format is `[3-bit opcode 010 meaning CALL] [8-bit call number]`. At a hunch, we try to call function `255` instead - and get `\x00` as output! We try changing some of the lower bits in the first instruction too, and get a different character in return. So the first instruction is `[3-bit opcode 110 meaning LOAD IMMEDIATE] [8-bit immediate value]`.

We do several calls to `255` in sequence, and get the same byte repeated multiple times. At this point we assume it's a register-based VM, and the call simply writes what's in the "main" register. Since it seems like the opcodes are 3 bits in size, we try various opcodes to provoke some interesting results. One of them, `100 xxxxxxxx`, seems to load a value from memory - which is the last section of the files. It reads from the memory cell at `[main register] + xxxxxxxx`, and this also leads us to discovering that memory cells are 64 bits in size. We also discover that the instruction `101 xxxxxxxx` is able to bring "back" older after repeated usages of `LOAD IMM` - the VM is stack-based after all!

We have now mapped 4 of the potential 8 "basic" opcodes. At this point we have enough to start writing a very basic disassembler - using it on the example programs seems to show that the disassembly goes off rails once it encounters a `111` instruction. Experiments show that instructions of the format `1110xyyyyyy` corresponds to bitshifts left or right with `yyyyyy` being the number of bits, and we also realize that stack registers are 64 bit too. Instructions of the format `1111xx` are the only 6-bit instructions in the VM, corresponding to `NOT`, `AND`, `OR` and `set if stack0 <= stack1`.

There are now three remaining opcodes, and we are stuck for a while. `011` seems to do nothing, while `000` and `001` seems to instantly abort the running program. It's not until we start looking closer at the disassembled programs that we notice that the value following `000` and `001` always have a matching value following a `011`. It turns out `011` sets a jump target in the code, and `000` is `jump if zero` and `001` is `jump`.

We are still missing a way to write data to memory, and again a deeper inspection of the disassembled code is needed - some times the "load memory" instruction uses an offset of `0x80` or higher - turns out the highest bit is not part of the offset, but means it's a write instruction instead. The same goes for the stack access instruction. We now have the full instruction set:

        000 xxxxxxxx    jmpz        n = pop(); if n == 0 then jump to labelxxxxxxxx
        001 xxxxxxxx    jmp         jump to labelxxxxxxxx
        010 xxxxxxxx    call        call function xxxxxxxx
        011 xxxxxxxx    label       set labelxxxxxxxx at current position
        1000 xxxxxxx    loadram     n = pop(); push(memory[n + xxxxxxx])
        1001 xxxxxxx    saveram     n = pop(); m = pop(); memory[n + xxxxxxx] = m
        1010 xxxxxxx    dup         n = pop(); m = stack[top-n-xxxxxxx]; push(m)
        1011 xxxxxxx    place       n = pop(); m = pop(); stack[top-n-xxxxxxx] = m
        110 xxxxxxxx    loadi       push(xxxxxxxx)
        11100 xxxxxx    shl         n = pop() << xxxxxx; push(n)
        11101 xxxxxx    shr         n = pop() >> xxxxxx; push(n)
        111100          not         n = pop(); push(~n)
        111101          and         n = pop(); m = pop(); push(n & m)
        111110          or          n = pop(); m = pop(); push(n | m)
        111111          setif       n = pop(); m = pop(); if m >= n then push(1) else push(0)
        
We can now write our own VM implementation, and a few hours later we've got the Brainfuck Interpreter running, and we're triumphantly staring at the output of "99 bottles".

----------

Now, with our own virtual machine, we can start studying `rev.cmp` in detail. We zero out all the example data in memory to see what a "blank" encryption looks like - and in the debug output of our VM we see a familiar constant scrolling by - `0x9e3779b9`. Could this be yet another implementation of the [Tiny Encryption Algorithm](https://en.wikipedia.org/wiki/Tiny_Encryption_Algorithm)? The ciphertext results don't match the reference implementation, though, but the constant and the left shifts by 4 and right shifts by 5 means it's something very similar.

We notice that the memory access pattern of the encryption keys is irregular - and remember that this is a property of the [XTEA](https://en.wikipedia.org/wiki/XTEA) algorithm, a slightly more advanced variant of TEA. And the ciphertexts matches with the result of the XTEA reference implementation.

But both these algorithms use XOR and addition - and those are not instructions in the VM? How do they do it? Turns out there's a way to build [XOR](http://bisqwit.iki.fi/story/howto/bitmath/#UsingNotOrAndAnd) and [addition](http://bisqwit.iki.fi/story/howto/bitmath/#UsingBitwiseOperationsWithXor) with just the AND, OR and NOT instructions, which the sample code uses. To decrypt we also need a way to do subtraction, but it's pretty easy to do: `a - b = a + (~b) + 1`

In addition to the previously built disassembler and VM, we also build a very basic assembler. With this we are able to create an XTEA decryption implementation, and after testing it locally thoroughly, we submit it, and finally get the flag - `hxp{W3-h4V3-to-60-D3ep3R}`
