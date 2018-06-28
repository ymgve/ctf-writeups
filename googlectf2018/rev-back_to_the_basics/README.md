# Back to the BASICs - Reversing - 293 points - 21 teams solved

> You won't find any assembly in this challenge, only C64 BASIC. Once you get the password,
> the flag is CTF{password}. P.S. The challenge has been tested on the VICE emulator.
>
> [Attachment](./734902061fdaade171291923c92df3a2bb7501f988da60022b8366f5e37137c0.zip)

The attachment contains a .PRG file, which means it is a single file Commodore 64 program (as opposed to a disk
or tape image). We download [VICE](http://vice-emu.sourceforge.net/) and run it. To make things faster, you can
go into the Autostart Settings and set `PRG autostart mode` to `Inject into RAM`, which means the emulator
won't emulate the slow loading from a disk drive. You can also use the `Alt+W` keys to toggle turbo mode, which
runs the emulator as fast as possible.

Running the PRG file, we are presented with a logo and a request for password. As a test, we just enter
garbage, and instantly get a `VERDICT: NOPE` in return, and the program freezes. We press `Caps Lock`, which is
what VICE maps to the [`RUN/STOP` key](https://www.c64-wiki.com/wiki/RUN/STOP), which stops the current running
BASIC program. Entering `LIST` gives us the listing of the current BASIC program:

    1 REM ======================
    2 REM === BACK TO BASICS ===
    3 REM ======================
    10 PRINTCHR$(155):PRINTCHR$(147)
    20 POKE 53280, 6:POKE 53281, 6:
    25 PRINT"LOADING..."
    30 DATA 2,1,3,11,32,32,81,81,81,32,32,32,32,81,32,32,32,32,81,81,81,81,32,81,81,81,81,81,32,32,81,81,81,81,32,32,87,87,87,87
    31 DATA 32,32,32,32,32,32,81,32,32,81,32,32,81,32,81,32,32,81,32,32,32,32,32,32,32,81,32,32,32,81,32,32,32,32,32,87,32,32,32,32
    32 DATA 20,15,32,32,32,32,81,81,81,32,32,81,32,32,32,81,32,32,81,81,81,32,32,32,32,81,32,32,32,81,32,32,32,32,32,32,87,87,87,32
    33 DATA 32,32,32,32,32,32,81,32,32,81,32,81,81,81,81,81,32,32,32,32,32,81,32,32,32,81,32,32,32,81,32,32,32,32,32,32,32,32,32,87
    34 DATA 20,8,5,32,32,32,81,81,81,32,32,81,32,32,32,81,32,81,81,81,81,32,32,81,81,81,81,81,32,32,81,81,81,81,32,87,87,87,87,32
    40 FOR I = 0 TO 39: POKE 55296 + I, 1: NEXT I
    41 FOR I = 40 TO 79: POKE 55296 + I, 15: NEXT I
    42 FOR I = 80 TO 119: POKE 55296 + I, 12: NEXT I
    43 FOR I = 120 TO 159: POKE 55296 + I, 11: NEXT I
    44 FOR I = 160 TO 199: POKE 55296 + I, 0: NEXT I
    50 FOR I = 0 TO 199
    51 READ C : POKE 1024 + I, C
    52 NEXT I
    60 PRINT:PRINT:PRINT:PRINT:PRINT
    70 POKE 19,1: PRINT"PASSWORD PLEASE?" CHR$(5): INPUT ""; P$: POKE 19,0
    80 PRINT:PRINT:PRINTCHR$(155) "PROCESSING... (THIS MIGHT TAKE A WHILE)":PRINT"[                    ]"
    90 CHKOFF = 11 * 40 + 1
    200 IF LEN(P$) = 30 THEN GOTO 250
    210 POKE 1024 + CHKOFF + 0, 86:POKE 55296 + CHKOFF + 0, 10
    220 GOTO 31337
    250 POKE 1024 + CHKOFF + 0, 83:POKE 55296 + CHKOFF + 0, 5
    2000 REM NEVER GONNA GIVE YOU UP
    2001 REM
    2010 POKE 03397, 00199 : POKE 03398, 00013 : GOTO 2001
    31337 PRINT:PRINT"VERDICT: NOPE":GOTO 31345
    31345 GOTO 31345
    
Quick intro to some BASIC specific concepts:

- `REM` is a comment line
- `DATA` declares an array of integers for later use
- `READ` fetches the next unread integer value from the declared arrays
- `POKE X, Y` places the byte `Y` into the memory address specified by `X`
- `PEEK(X)` is the current byte in memory address `X`
- Even though some numbers start with `0`, they are not octal, they are decimal

Quick intro to the Commodore 64 memory layout, the parts used in this program:

    0400-07e7  1024- 2023 Screen memory, 40x25 characters
    0801-9fff  2049-49059 Default location for BASIC program storage
    d020-d021 53280-53281 Border color and background color
    d800-dbe7 55296-56295 Screen color memory, 40x25 characters
    
This is what the program does, summarized:

- Line 1-60 of the program prints the logo
- Line 70 places your password in the variable `P$`
- Line 200 checks if your entered password is 30 characters long, continues to line 250 if true
- Line 210-220 draws a red X in the progress bar, then continues at line 31337
- Line 250 draws a green heart in the progress bar
- Line 2010 writes some values into BASIC memory, where the program is stored, then goes to line 2001
- Line 31337-31345 prints an error message, and enters an endless loop.

To understand what happens at line 2010, let's take a look at how BASIC programs are stored in C64 memory. Each
line starts with two 16-bit little endian values, the first is a pointer to the memory address of the next line
(Or zero if the end of the program), then the line number. After that follows a null terminated string of
PETSCII characters, but with reserved words replaced with [characters above
0x80](https://www.c64-wiki.com/wiki/BASIC_token) to save space.

We created a [small script](./print_programs.py) that lists the BASIC program from outside the emulator, this time including the
current and next memory addresses of each line:

    0801 081e 1 REM ======================
    081e 083a 2 REM === BACK TO BASICS ===
    083a 0857 3 REM ======================
    0857 086b 10 PRINTCHR$(155):PRINTCHR$(147)
    086b 0886 20 POKE 53280, 6:POKE 53281, 6:
    0886 0898 25 PRINT"LOADING..."
    0898 0913 30 DATA 2,1,3,11,32,32,81,81,81,32,32,32,32,81,32,32,32,32,81,81,81,81,32,81,81,81,81,81,32,32,81,81,81,81,32,32,87,87,87,87
    0913 0991 31 DATA 32,32,32,32,32,32,81,32,32,81,32,32,81,32,81,32,32,81,32,32,32,32,32,32,32,81,32,32,32,81,32,32,32,32,32,87,32,32,32,32
    0991 0a0f 32 DATA 20,15,32,32,32,32,81,81,81,32,32,81,32,32,32,81,32,32,81,81,81,32,32,32,32,81,32,32,32,81,32,32,32,32,32,32,87,87,87,32
    0a0f 0a8d 33 DATA 32,32,32,32,32,32,81,32,32,81,32,81,81,81,81,81,32,32,32,32,32,81,32,32,32,81,32,32,32,81,32,32,32,32,32,32,32,32,32,87
    0a8d 0b09 34 DATA 20,8,5,32,32,32,81,81,81,32,32,81,32,32,32,81,32,81,81,81,81,32,32,81,81,81,81,81,32,32,81,81,81,81,32,87,87,87,87,32
    0b09 0b2f 40 FOR I = 0 TO 39: POKE 55296 + I, 1: NEXT I
    0b2f 0b57 41 FOR I = 40 TO 79: POKE 55296 + I, 15: NEXT I
    0b57 0b80 42 FOR I = 80 TO 119: POKE 55296 + I, 12: NEXT I
    0b80 0baa 43 FOR I = 120 TO 159: POKE 55296 + I, 11: NEXT I
    0baa 0bd3 44 FOR I = 160 TO 199: POKE 55296 + I, 0: NEXT I
    0bd3 0be5 50 FOR I = 0 TO 199
    0be5 0bfd 51 READ C : POKE 1024 + I, C
    0bfd 0c05 52 NEXT I
    0c05 0c13 60 PRINT:PRINT:PRINT:PRINT:PRINT
    0c13 0c4a 70 POKE 19,1: PRINT"PASSWORD PLEASE?" CHR$(5): INPUT ""; P$: POKE 19,0
    0c4a 0c9e 80 PRINT:PRINT:PRINTCHR$(155) "PROCESSING... (THIS MIGHT TAKE A WHILE)":PRINT"[                    ]"
    0c9e 0cb7 90 CHKOFF = 11 * 40 + 1
    0cb7 0cd0 200 IF LEN(P$) = 30 THEN GOTO 250
    0cd0 0d05 210 POKE 1024 + CHKOFF + 0, 86:POKE 55296 + CHKOFF + 0, 10
    0d05 0d11 220 GOTO 31337
    0d11 0d45 250 POKE 1024 + CHKOFF + 0, 83:POKE 55296 + CHKOFF + 0, 5
    0d45 0d63 2000 REM NEVER GONNA GIVE YOU UP
    0d63 0d69 2001 REM
    0d69 0d96 2010 POKE 03397, 00199 : POKE 03398, 00013 : GOTO 2001
    0d96 0db5 31337 PRINT:PRINT"VERDICT: NOPE":GOTO 31345
    0db5 0dc1 31345 GOTO 31345
 
Now let's take a look at line 2010 again. It places two bytes at address `0d45-0d56`, which is the next-line 
pointer for line 2000, which originally points at `0d63`. The full 16 bit value stored is 199 + 13 * 256 =
3527, or `0dc7` in hex. This means after this, the lines after 2000 and onwards will now be *different*. We do
a new listing of the program, after the bytes have changed:

    ....
    0cb7 0cd0 200 IF LEN(P$) = 30 THEN GOTO 250
    0cd0 0d05 210 POKE 1024 + CHKOFF + 0, 86:POKE 55296 + CHKOFF + 0, 10
    0d05 0d11 220 GOTO 31337
    0d11 0d45 250 POKE 1024 + CHKOFF + 0, 83:POKE 55296 + CHKOFF + 0, 5
    0d45 0dc7 2000 REM NEVER GONNA GIVE YOU UP
    0dc7 0deb 2001 POKE 03397, 00069 : POKE 03398, 00013
    0deb 0e1f 2002 POKE 1024 + CHKOFF + 1, 81:POKE 55296 + CHKOFF + 1, 7
    0e1f 0e46 2004 ES = 03741 : EE = 04981 : EK = 148
    0e46 0e81 2005 FOR I = ES TO EE : K = ( PEEK(I) + EK ) AND 255 : POKE I, K : NEXT I
    0e81 0e9d 2009 POKE 1024 + CHKOFF + 1, 87
    0e9d 7a57 29510 (garbage data)
    
We get garbage data after a few lines. Does our listing program have a bug somewhere, or is something else
going on? Let's take a closer look at the new readable lines:

- Line 2001 now sets the pointer of line 2000 to `0d45`, which means it now points to itself
- Line 2002 draws a filled yellow dot in the progress bar
- Line 2004-2005 does something to a range of bytes in BASIC memory
- Line 2009 draws an outlined yellow dot in the progress bar

One thing to note is that all this in-memory manipulation is possible because BASIC doesn't really check where
a specific numbered line is in memory until strictly necessary, that is, when a `GOTO` is executed. So the
change at the new line 2001 for example won't have any immediate effects - the interpreter still follows the
same linked list of line numbers that it's currently on, even though predecessors in the list have been
changed.

But what is the point of the 2001 line? It basically seems to be an anti-debugging trick - if we try to use
`RUN/STOP` and `LIST` after this line has been executed, we will just get an endless listing of
`2000 REM NEVER GONNA GIVE YOU UP`.

The 2004-2005 lines are the most interesting. A closer examination shows that it adds 148 to each byte in the
range `0e9d`-`1375` - it is actually deobfuscating the rest of the BASIC program that follows after line 2009.
Let's do this deobfuscation, and see what we get:

    ....
    0e1f 0e46 2004 ES = 03741 : EE = 04981 : EK = 148
    0e46 0e81 2005 FOR I = ES TO EE : K = ( PEEK(I) + EK ) AND 255 : POKE I, K : NEXT I
    0e81 0e9d 2009 POKE 1024 + CHKOFF + 1, 87
    0e9d 0eeb 2010 V = 0.6666666666612316235641 - 0.00000000023283064365386962890625 : G = 0
    0eeb 0f05 2020 BA = ASC( MID$(P$, 1, 1) )
    0f05 0f1f 2021 BB = ASC( MID$(P$, 2, 1) )
    0f1f 0f7e 2025 P0 = 0:P1 = 0:P2 = 0:P3 = 0:P4 = 0:P5 = 0:P6 = 0:P7 = 0:P8 = 0:P9 = 0:PA = 0:PB = 0:PC = 0
    0f7e 0fbc 2030 IF BA AND 1 THEN P0 = 0.062500000001818989403545856475830078125
    0fbc 0ffb 2031 IF BA AND 2 THEN P1 = 0.0156250000004547473508864641189575195312
    0ffb 103a 2032 IF BA AND 4 THEN P2 = 0.0039062500001136868377216160297393798828
    103a 1079 2033 IF BA AND 8 THEN P3 = 0.0009765625000284217094304040074348449707
    1079 10b9 2034 IF BA AND 16 THEN P4 = 0.0002441406250071054273576010018587112427
    10b9 10f9 2035 IF BA AND 32 THEN P5 = 0.0000610351562517763568394002504646778107
    10f9 1139 2036 IF BA AND 64 THEN P6 = 0.0000152587890629440892098500626161694527
    1139 117a 2037 IF BA AND 128 THEN P7 = 0.0000038146972657360223024625156540423632
    117a 11b9 2040 IF BB AND 1 THEN P8 = 0.0000009536743164340055756156289135105908
    11b9 11f8 2031 IF BB AND 2 THEN P9 = 0.0000002384185791085013939039072283776477
    11f8 1237 2032 IF BB AND 4 THEN PA = 0.0000000596046447771253484759768070944119
    1237 1275 2033 IF BB AND 8 THEN PB = 0.000000014901161194281337118994201773603
    1275 12b5 2034 IF BB AND 16 THEN PC = 0.0000000037252902985703342797485504434007
    12b5 1300 2050 K = V + P0 + P1 + P2 + P3 + P4 + P5 + P6 + P7 + P8 + P9 + PA + PB + PC
    1300 131a 2060 G = 0.671565706376017
    131a 133b 2100 T0 = K = G : A = 86 : B = 10
    133b 135a 2200 IF T0 = -1 THEN A = 83 : B = 5
    135a 1376 2210 POKE 1024 + CHKOFF + 1, 90
    1376 137c 2500 REM
    137c 13b7 2900 FOR I = ES TO EE : K = ( PEEK(I) + EK ) AND 255 : POKE I, K : NEXT I
    13b7 13ea 2905 POKE 1024 + CHKOFF + 1, A:POKE 55296 + CHKOFF + 1, B
    13ea 1417 2910 POKE 03397, 00029 : POKE 03398, 00020 : GOTO 2001
    
That's a lot of new stuff! Let's examine it closer:

- Line 2010 sets a floating point variable `V`
- Line 2020-2021 takes the character values from the first and second characters in your password and places them in variables `BA` and `BB` (Note, BASIC is 1-indexed, not 0-indexed)
- Line 2025-2034 sets 13 different floating point variables, depending on whether the corresponding bits in `BA` and `BB` were set
- Line 2050-2100 adds all the values together and compares it with the goal variable `G`. Note the construction `TO = K = G`, which actually means `T0 = (K == G)` in other languages - sets `T0` to true (-1) or false (0)
- Line 2900 re-obfuscates the previously de-obfuscated lines
- Line 2905 draws a character in the progress bar, either a red X for failure or green heart for success
- Line 2910 sets the line 2000 next line pointer to address `141d`, then goes back to line 2001

So the program uses floating point values to obfuscate the correct bits that should be set in the password. But
it doesn't really do anything with the result of the calculation yet, apart from drawing on the screen.

While running this check, the `NEVER GONNA GIVE YOU UP` endless loop is still in effect. So listing these lines
from inside the emulator isn't possible. Right before the line 2000 pointer is re-written, line 2900
re-obfuscates the check part, so at no point in time will a `RUN/STOP` expose the actual bit check code.

But let's see what happens after line 2910 has executed. We've got a new listing:

    ....
    0d45 141d 2000 REM NEVER GONNA GIVE YOU UP
    141d 1441 2001 POKE 03397, 00069 : POKE 03398, 00013
    1441 1475 2002 POKE 1024 + CHKOFF + 2, 81:POKE 55296 + CHKOFF + 2, 7
    1475 149c 2004 ES = 05363 : EE = 06632 : EK = 152
    149c 14d7 2005 FOR I = ES TO EE : K = ( PEEK(I) + EK ) AND 255 : POKE I, K : NEXT I
    14d7 14f3 2009 POKE 1024 + CHKOFF + 2, 87
    14f3 7da9 28482 (garbage data)

It's basically the same as the earlier listing, only with a few parameters changed. This time, it deobfuscates
the memory area `14f3`-`19e8`. Listing after deobfuscation:

    ....
    1475 149c 2004 ES = 05363 : EE = 06632 : EK = 152
    149c 14d7 2005 FOR I = ES TO EE : K = ( PEEK(I) + EK ) AND 255 : POKE I, K : NEXT I
    14d7 14f3 2009 POKE 1024 + CHKOFF + 2, 87
    14f3 1541 2010 V = 0.6666666666612316235641 - 0.00000000023283064365386962890625 : G = 0
    1541 155b 2020 BA = ASC( MID$(P$, 2, 1) )
    155b 1575 2021 BB = ASC( MID$(P$, 3, 1) )
    1575 158f 2022 BC = ASC( MID$(P$, 4, 1) )
    158f 15ee 2025 P0 = 0:P1 = 0:P2 = 0:P3 = 0:P4 = 0:P5 = 0:P6 = 0:P7 = 0:P8 = 0:P9 = 0:PA = 0:PB = 0:PC = 0
    15ee 162d 2030 IF BA AND 32 THEN P0 = 0.062500000001818989403545856475830078125
    162d 166d 2031 IF BA AND 64 THEN P1 = 0.0156250000004547473508864641189575195312
    166d 16ae 2032 IF BA AND 128 THEN P2 = 0.0039062500001136868377216160297393798828
    16ae 16ed 2033 IF BB AND 1 THEN P3 = 0.0009765625000284217094304040074348449707
    16ed 172c 2034 IF BB AND 2 THEN P4 = 0.0002441406250071054273576010018587112427
    172c 176b 2035 IF BB AND 4 THEN P5 = 0.0000610351562517763568394002504646778107
    176b 17aa 2036 IF BB AND 8 THEN P6 = 0.0000152587890629440892098500626161694527
    17aa 17ea 2037 IF BB AND 16 THEN P7 = 0.0000038146972657360223024625156540423632
    17ea 182a 2040 IF BB AND 32 THEN P8 = 0.0000009536743164340055756156289135105908
    182a 186a 2031 IF BB AND 64 THEN P9 = 0.0000002384185791085013939039072283776477
    186a 18ab 2032 IF BB AND 128 THEN PA = 0.0000000596046447771253484759768070944119
    18ab 18e9 2033 IF BC AND 1 THEN PB = 0.000000014901161194281337118994201773603
    18e9 1928 2034 IF BC AND 2 THEN PC = 0.0000000037252902985703342797485504434007
    1928 1973 2050 K = V + P0 + P1 + P2 + P3 + P4 + P5 + P6 + P7 + P8 + P9 + PA + PB + PC
    1973 198d 2060 G = 0.682612358126820
    198d 19ae 2100 T1 = K = G : A = 86 : B = 10
    19ae 19cd 2200 IF T1 = -1 THEN A = 83 : B = 5
    19cd 19e9 2210 POKE 1024 + CHKOFF + 2, 90
    19e9 19ef 2500 REM
    19ef 1a2a 2900 FOR I = ES TO EE : K = ( PEEK(I) + EK ) AND 255 : POKE I, K : NEXT I
    1a2a 1a5d 2905 POKE 1024 + CHKOFF + 2, A:POKE 55296 + CHKOFF + 2, B
    1a5d 1a8a 2910 POKE 03397, 00144 : POKE 03398, 00026 : GOTO 2001
    
Yet again, we see the same code as before with a few parts changed. Most notably, the floating point constants
appear to be the *same*, which means there hopefully is a pattern here.

This sequence of redirecting program flow and deobfuscating sections repeats 19 times, until we finally arrive
at the last code sequence:

    ....
    0d45 86ef 2000 REM NEVER GONNA GIVE YOU UP
    86ef 86f5 2001 REM
    86f5 875a 31337 T = T0 + T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8 + T9 + TA + TB + TC + TD + TE + TF + TG + TH + TJ
    875a 8772 31338 IF T = -19 THEN GOTO 31340
    8772 8791 31339 PRINT:PRINT"VERDICT: NOPE":GOTO 31345
    8791 87ab 31340 PRINT:PRINT"VERDICT: CORRECT"
    87ab 87b7 31345 GOTO 31345
    
A quick look through the 19 verification steps shows that all the bit constants are the same, as we suspected -
the `V` value seems to be slightly different in some cases, though. Crossing our fingers, we isolate all the
`G` variables, and try to create [a solver in Python](./solution.py). While C64 BASIC uses 40-bit integers, we hope that there's
enough similarity to PC integers that it won't be a problem.

The solver exploits the fact that each bit is much larger than the next one, so we try to subtract each bit
from the target value in decreasing order, and if the result is positive, we mark the corresponding bit as set
and use the result as the new target value.

Thankfully, the script worked perfectly, and it printed the password `LINKED-LISTS-AND-40-BIT-FLOATS` without
any errors, with the full flag being `CTF{LINKED-LISTS-AND-40-BIT-FLOATS}`.
