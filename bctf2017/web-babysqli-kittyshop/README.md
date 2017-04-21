# Baby Sqli - web
> Come on Baby!
> http://baby.bctf.xctf.org.cn/

# Kitty Shop - web
> Kitty shop or flag shop
> http://baby.bctf.xctf.org.cn/

This challenge had multiple flags on a single website. It actually contains 3 flags, but no one managed to solve the reverse engineering "Flag Shop" challenge.

The first problem was bypassing the login screen. Almost everything useful for SQL injection was filtered by a [Web Application Firewall](https://en.wikipedia.org/wiki/Web_application_firewall) - the username field allowed newlines which could then be used instead of spaces and tab characters, which were blocked, but any attempt at more complex SQL statements were met with failure. Eventually I stumbled upon the extremely simple `'\n#` input, which allowed me to login. Here, I was greeted with a shop where I could buy some things, but no flag in sight. Also there was a ReCaptcha for every purchase you wanted to make, so scripting was out of the question. There was also a weird "manual" link that used the script `load.php` - this script had a local file injection vulnerability, and I was able to list `../../../../../../../../../../etc/passwd` - but still no flag to be found. This LFE also seemed to block any file name with `php` in it, so I was unable to get the source of the web app.

Eventually I stumbled upon the `.viminfo` file, which further pointed to the file `app/encrypt0p@ssword/password`. After some more guessing I found that accessing `../encrypt0p@ssword/password` worked, and got a file that contained a link to a server side binary and the password `c1i3nt_B@ckup`. Finally, inside the binary was the flag for "Baby SQLI" - turns out you were supposed to modify the purchase request and purchase item "D" on the website to get the flag.

The second flag was even more elusive. The binary seemed to connect to another server at port 8080 then did some crypto stuff/signature verification when you picked option "B", but running it just gave an error - the same error you got if you tried option "B" directly on the website. The actual server address it connected to was encrypted with simple XOR - I decrypted it and got the address http://202.112.51.232:8888/pcap . Visiting this site allowed me to download what seemed to be a full packed capture of all service traffic at port 8080, but this didn't bring me any closer to the second flag.

Finally, on a hunch, I fired up tcpdump and looked at the raw TCP traffic being exchanged when I ran the binary, and there it was - the second flag, in plain text. Seems like it was just the signature that was intentionally broken.
