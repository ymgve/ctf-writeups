# Proprietary Format - Reversing - 326 points - 19 teams solved

> The villains are communicating with their own proprietary file format. Figure out what it is.
>
> $ nc proprietary.ctfcompetition.com 1337
>
> [Attachment](./c0f3178a1f16d1a2c8b281fd8cd10b24da2fc9eafa551664f73357efe091f189.zip)

The attachement is a file named `flag.ctf` - looking at it in a hex editor I saw four magic bytes `GCTF` at the
start, then little endian 32 bit values corresponding to `600` and `400` - so I assumed it was some kind of
picture format.

At first I completely missed that there was a network address in the challenge description, so I spent a lot of
time doing analysis of the content of the file. It seemed like some kind of stream format - each "element" was a
byte in the range `0x00`-`0x0f`, where all elements except `0x0f` was followed by a 3-byte value. Interpreting
these 3-byte values in isolation as RGB pixels gave some garbled pastel colored gradients, which suggested that
the picture format assumption was correct.

Due to lack of progress I dropped the challenge until near the end of the contest, when someone made me aware of
the network address. After a bit of error message guided fuzzing, I found out that the service first required
three lines each terminated by `LF`, first the format specifier `P6`, then the width and height of the picture,
like `320 240`, and finally some unknown value that always had to be `255`. Then it read in width*height raw RGB
pixel values, and in return it sent the picture encoded in the proprietary format.

With a reference encoder, I finally made some progress. I quickly realized that it was some kind of 2D based
lossy encoding, but couldn't figure out the specifics before time ran out.

Some days after the contest I realized what was missing from the puzzle and managed to write a decoder. First,
find the largest power of 2 square that can fit the entire picture - in the case of `flag.ctf` this is a
`1024x1024` pixel square. Then, split the picture into quadrants, and read the first "command" byte. Here, each
bit corresponds to a`512x512` pixel quadrant:

    1 2
    4 8
    
where a set bit means that you should recursively parse that quadrant, and a cleared bit means that you should
paint the entire quadrant with the color following after the command byte. (Since `0x0f` means recursively parse
all quadrants, no color follows it.)

As an example, this is the format of the sample file, excluding the 12 byte header:

    03 000000 [upper left quadrant data] [upper right quadrant data]

This means that the definition of the upper left `512x512` block comes first, then the definition of the upper
right block. The bottom blocks are painted entirely black, as that's the color following the command. As the
original picture was only `400` pixels high, this makes sense.

With this information, I was able to write a [picture decoder](./proprietary_decoder.py), and finally exctract
the flag `CTF{P1c4Ss0_woU1d_B3_pr0UD}`
