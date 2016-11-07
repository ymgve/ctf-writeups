# APTeaser - Reversing - 300 points

>The Trump campain is suddenly able to predict our every move. We believe that they hired either Russia or one of those 400 lb hackers to compromise our staff systems.
>
>Find out what information they stole and how!
(No, it's not one of /those/ pcap challenges)
>
>apteaser
>
>author's irc nick: clark

We are given a packet capture, and we start with the TCP conversation list in Wireshark. Sorting by number of outgoing
bytes, a strange stream shows up - sending 184kbytes on port `27015`. Opening the stream in an hex editor shows a curious
pattern - it looks like a JPEG image where half the bytes are corrupted/encrypted while the other half are left alone. After
a bit of failing to find some pattern in the encrypted bytes, we decide to go look for the malware instead. Knowing that it
has to be in the capture before the exfiltration stream started cuts significantly down on the number of packets that need
to be examined.

We soon discover a file called `12840_docs_acherb99HA03meE0.pdf` from host `important.documents.trustme` which is *actually*
an EXE file. We load it up in IDA, and look for any functions related to `send()` since we know it sent the data out over
TCP, and find an interesting function at `0x004027E0`. The function takes a buffer as input, and for each chunk of `0x800`
bytes it uses `srand()` with the current time, then uses `rand()` to generate a keystream that is XORed with the buffer, and
sleeps for 0 to 3600 milliseconds. This explains the odd patterns in the encrypted file, since under Windows, `rand()` only
creates 16 bit random numbers.

We write a small Windows program that tries random seeds until it finds the correct value that generates the expected JPEG headers,
and know that we are successful when the upper line of a screenshot is shown in the decrypted image. Since each `0x800` byte block
has a new seed, and we know it is seeded from the current time, each call to `srand()` should be 0 to 4 higher than the previous
call. We then brute force it block by block, increasing the seed value until we get an image with no broken JPEG patterns.
Eventually enough of the screenshot is revealed that we can read the flag - `flag{1_n33d_my_t00Lb4r5}`
