# ASIS secret letter - Misc/Stego - 202 points - 17 solvers

> The face is the index of the mind, its ASIS [secret](./asis_letter_ee08c0c4f40b815277393c4e3f3966bd240bc4f9) letter!

There are two images in the download in the description, one JPG and one PNG. We don't see any immediate hidden messages when the files are viewed in a hex editor, but when viewing the JPG we notice that it contains EXIF metadata. There is an "ImageDescription" tag which contains apparent garbage. Re-opening in a hex editor, we see that the garbage starts with `\x78\x9C` which could be a header for compressed zlib data. So we write a small script that decompresses, and it works! We get a piece of base64 encoded data, which we have to base64 decode a few times recursively before we get the message "??  from ASIS with love, please find secret message and reply soon, powered by ??  Stéganô ??".

We install [Stegano](https://github.com/cedricbonhomme/Stegano) as hinted, and try various options and discover that `stegano-lsb-set reveal -i e07d17ed7d8104590ff3e17bdf052057 --generator triangular_numbers` reveals the flag: `ASIS{767ba85340d9e49fa0bb9c2b12037f08}`
