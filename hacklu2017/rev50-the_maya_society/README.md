# The Maya Society - Reversing - 50 points

> Maya society was broken into a class structure with four main levels: the nobility (Maya almehenob), the priesthood (Maya ahkinob), the common people (Maya ah chembal uinieol), and the slaves (Maya ppencatob). The most powerful of the ruling elite was known as the halach uinic. The halach uinic are alive and still secretly hold meetings today. You have to reverse engineer their communication and infiltrate the ruling elite. [Link](./launcher)

Link originally pointed to a website, [screenshot here](./images/website.jpg). The download gave use a 64-bit ELF.

Loading it up and decompiling in IDA shows us this at the top of the function:

![decompiled](./images/disassembly.png)

The string `.fluxfingers.net` points towards something related to a domain name. Next, the current time is used, and formatted like `2017-10-19`. Then there's some hash function(?) that we never bothered reversing.

A date. And Mayas. [Hmmmm.](https://en.wikipedia.org/wiki/2012_phenomenon)

We set the current time of our box to December 21st 2012, which was supposed to be "end of the world for the Mayas" according to tabloids everywhere, and simply run the program. In return, we get the flag, `flag{e3a03c6f3fe91b40eaa8e71b41f0db12}`.

(Another hint that we had to change the date can be seen on the website screenshot - it links to "13.0.0.0.0" which is the Mayan calendar date that equals Dec 21st 2012)
