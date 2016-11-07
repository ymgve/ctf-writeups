# Warp Speed - Forensics - 150 points

> Our Trump advertising campaign is incredible, it's skyrocketing! It's astronomical! Wait stop!! SLOW DOWN!!!
> 
> warp_speed
> 
> author's irc nick: krx

Distorted image. Can see image is split into lines that are 8 pixels high. Consider them all part of a 8 pixel high,
very long line instead. Experimenting a bit, re-splitting the line into segments of length 504 pixels gives a
undistorted image, revealing the flag `flag{1337_ph0t0_5k1ll5}`
