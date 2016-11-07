# More Suspicious Traffic - Forensics - 300 points

>We think our voting computers might be compromised! The Clinton campaign claims Trump is working with the Russians to rig the election. Our tech got a packet capture right before strange things started happening and isolated these packets. Our IDS didn't flag anything, but take a look and see if you can find any hidden communications channels the Russians could use for command and control (C2). It would make the leaders of the free world look pretty bad if the Russians were the ones picking our president!
> 
> SecureFloridaVotingBoothTraffic
> 
> author's irc nick: LtDan

Packet capture of UDP traffic between two hosts.Pattern is that one host sends some UDP packets (with identical content) then the other host responds with some UDP packets (with identical content) within a short timeframe. Then traffic stops for either 500 or 1500 milliseconds.

After looking a while at this pattern, it became clear that it was Morse code, with 6 packets in a timeframe meaning a `.` and 12 packets in a timeframe meaning `_`, and a 500 millisecond pause between each Morse symbol, while a 1500 millisecond pause meant a break between individual Morse code letters. Final code was `..-. .-.. .- --. -.--. .... ....- -.-. -.- --... .... ...-- .--. .-.. ....- -. ...-- --... -.--.-` which becomes the flag `flag{h4ck7h3pl4n37}`
