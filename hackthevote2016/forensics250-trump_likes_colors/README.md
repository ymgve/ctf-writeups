# Trump likes colors - Forensics - 250 points

> Somebody leAked TrumP's favorite colors, looks like they used a really esoteric format. Some chiNese hacker named "DanGer Mouse" provided us the leak, getting this crucial info could really sway voters at the polls!
> 
> trump_likes_colors.png
> 
> author's irc nick: nihliphobe

Hints here are the capitalized letters "APNG" and "esoteric". The file is an APNG animation with 16384 frames, each of the frames being a program for the [Piet](http://www.dangermouse.net/esoteric/piet.html) esoteric 2D programming language. Each of the programs output a color in HTML format, like `#ff0000`, which can then be combined into a 128*128 pixel image which itself is a new Piet program. Didn't find a good program to convert APNG into frames (FFmpeg gave bad results), so had to hack together a script to extract hex values directly.

Also had to edit the final image slightly, as the created image lacked the `out(char)` colors between stack `pop`'s. Final flag was `flag{7h15_w45n7_3v3n_4_ch4ll3n63._54d_.}`
