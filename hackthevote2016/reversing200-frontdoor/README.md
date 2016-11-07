# Frontdoor - Reversing - 200 points

>Alex Jones here. We all know Crooked Clinton has rigged the election. The establishment is afraid of Trump! But Trump has heard our call, he knows the history of fraud, he knows how they tried to steal the primaries from him,and how they did steal it from Bernie Sanders, unfortunately. So now he needs your help fellow patriot. Help us unrig these establishment owned voting machines, one polling station at a time!
>
>Now we have got some of the best people together, and have found that they are using a camera that clearly wasn't made in the US of A. Clearly the Dems have already rigged this station. See if you can't find a way in though that immigrant camera. I'm sure you can't fail with the help of some official INFOWARS branded BRAIN FORCE(tm) now available for only 22.46 (limited time only.)
>
>frontdoor
>
>http://surveillance.pwn.democrat/
>
>author's irc nick: itszn
>
>Brain Force(tm) now just 29.95 http://store.infowars.com/Brain-Force_p_1611.html

The given file is a romfs file system which can easily be mounted via the standard `mount` command. It's a uClinux distro,
but one of the things that stand out is the `/bin/camera` file. It's a `bFLT` binary, and while IDA supports them, they
can't be loaded in a compressed form. Found a script called `gunzip_bflt.pl` that extracts, and now IDA can load it (After
remembering to set ARM as architecture).

Since we have been given a web URL and other ports like ftp and telnet seem to be filtered, we focus reversing on the web
component. The most promising function is at `0x00014E68` which calls different handlers depending on what .cgi URL we're
accessing. All of them except one - http://surveillance.pwn.democrat/get_status.cgi - are protected by HTTP auth. After
failing to find some flaw in the HTTP authentication code, we realize that there is also an alternate authentication scheme
via URL parameters which is checked individually inside each URL handler. We notice that the handler for `snapshot.cgi` uses
a different function than the others, one at `0x00021BB8` ...and it contains *weird hex and XOR*!

We write a simple script that extracts the backdoor username and password, and we find out that visiting
http://surveillance.pwn.democrat/snapshot.cgi?B4cKD00rdCam=H4ck3rA774ck bypasses the auth and gives us an image - with the
flag `flag{B4CK_D0OR_A1L_7h3_107!4_R3AL!}` written on a whiteboard.
