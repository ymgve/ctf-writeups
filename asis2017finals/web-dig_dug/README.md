# Dig Dug - Web - 29 points - 243 solvers

> The pot calling the [kettle](https://digx.asisctf.com/) black.

Visiting the website in the description shows us a pretty picture and the quote "If you want to know what is dig, you should consider that dig stands for domain information groper." This refers to the [dig](https://linux.die.net/man/1/dig) Unix tool, which lets you see various DNS properties for a domain.

We run `dig digx.asisctf.com` but don't see anything interesting.

    ;; ANSWER SECTION:
    digx.asisctf.com.       300     IN      A       192.81.223.250

But the challenge is called dig**x**, so we try the reverse DNS lookup option `dig -x 192.81.223.250`

    ;; ANSWER SECTION:
    250.223.81.192.in-addr.arpa. 1800 IN    PTR     airplane.asisctf.com.

Hmm. Another website on the same IP. We visit the site, and get the text "hi all, you should go offline to get the flag... Enable Airplane Mode". We do as the instructions tells us, visiting `airplane.asisctf.com` via our phone, then enable airplane mode on the phone. And sure enough, this gives us a flag! `ASIS{_just_Go_Offline_When_you_want_to_be_creative_!}`
