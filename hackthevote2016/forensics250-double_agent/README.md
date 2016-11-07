# Double Agent - Forensics - 250 points

> We have a man on the inside of Trump's campaign, but he's too afraid to leak secrets through normal communication methods. He swapped out the normal font on the campaign website for this one, and we suspect his data is inside.
> 
> lexicographic.otf
> 
> author's irc nick: Lense
> 
> EDIT: We provided the font. You do not need to go to any website to solve this.
> 
> Inspired by http://www.sansbullshitsans.com

Installed [FontForge](https://fontforge.github.io/en-US/) then opened the font. At unicode codepoint `U+0400` and onwards
there are some letters that look they might be part of a flag. (Especially because they include `f`,`l`,`a`,`g`,`{` and `}`)

<p align="center">
<img src="https://raw.githubusercontent.com/ymgve/ctf-writeups/master/hackthevote2016/forensics250-double_agent/overview.png">
</p>

Looking at the properties of the glyph, then the ligatures subpanel shows some weird ligatures

<p align="center">
<img src="https://raw.githubusercontent.com/ymgve/ctf-writeups/master/hackthevote2016/forensics250-double_agent/ligatures.png">
</p>

Looking at which ligatures correspond to which letters, then sorting them like

    AAAA f
    BBBB l
    CCCC a
    DDDD g
    
and so on gives the final flag `flag{itsallintheligatures}`