# Madlog - Crypto - 200 points - 4 solvers

> Acid Burn broke into The Plague's home wifi and found, deep down in the darkness of the subnets, a server which emits peculiar data. Can you help her to compromise the server?
>
> Solves: 4
>
> Service: nc crypto.sect.ctf.rocks 31337
>
> Author: grocid

When we connect to the server, we are presented with a menu for requesting plaintexts and submitting. Sample session:

    > nc crypto.sect.ctf.rocks 31337
    madlog server starting...
    Options:
    1. Request plaintext...
    2. Submit...
    1
    q^e mod p = a
    g = 201527
    e = 170889198766265986594054717664789561344
    p = 156920319682269547550840440422064789702830774969897260932124088315247211163110865017305817005797304213752612556763228047723789794713560055335007282974774888
    844332820576469678725018919853260647462367864702092052584778617621806467695299678199684012931325300660671488872927592192102428093535426026544017575524159
    a = 149487841952747588106070346976004484066065895016918064204696247058119061554741530705085905723976501055498909092832058610177675891420269200781184130110986764
    623289893864930014158982791705565650689999251993360069827833690069334186086036528157206789003293998862601492326728199651838658908930802147366865434202266
    Options:
    1. Request plaintext...
    2. Submit...
    2
    q^e mod p = a
    g = 201527
    p = 156920319682269547550840440422064789702830774969897260932124088315247211163110865017305817005797304213752612556763228047723789794713560055335007282974774888
    844332820576469678725018919853260647462367864702092052584778617621806467695299678199684012931325300660671488872927592192102428093535426026544017575524159
    a = 597934094089076143532715697600650370614454179755840791824457637108751510297208242434790303573192467040580829131109745276608239407552985180349820088145066583
    2272019838798959446341805023813722554319877078103052572044138787266038718089266541619645975672452627374869278026996124184443323039815597938556981195604
    Gimme e... you have 180 seconds!
    
After a question to the organizers it was clarified that there is a typo and `q` is supposed to be `g`. So this is a [Discrete logarithm](https://en.wikipedia.org/wiki/Discrete_logarithm) challenge. `e` is pretty large, so unless there is some trick, it seems impossible. But we take a second look at `e`, this time in hexadecimal:

    170889198766265986594054717664789561344 = 0x80901000800000000000402450008000
    
Hmm. That's a LOT of zero bytes. And some of the remaining bytes also seem slightly odd.

After getting more plaintexts, we see a pattern: each number will be 128 bits, have at most 11 bits set, with 1 << 127 always being set and the last bit always being cleared. Again the example number, this time in binary:

    0b10000000100100000001000000000000100000000000000000000000000000000000000000000000010000000010010001010000000000001000000000000000

This must be exploitable somehow! We also notice that `g` and `p` never change. After some thinking we come up with a way to use the [Baby-step Giant-step](https://en.wikipedia.org/wiki/Baby-step_giant-step) algorithm:

* Precompute a large database of `m, e1` pairs where `m = q^e mod p` and `e1` got 5 random bits between 1 and 126 set
* Connect and get the target `a`
* Randomly generate a number `e2` with 1 << 127 and 5 other random bits between 1 and 126 set
* Compute `m = a * (q^-1)^e2 mod p` and see if the result is in our precomputed database
* If not found, repeatedly generate new `e2` and compute `m` until a match is found, or time limit expires
* If time limit expires, reconnect and get a new `a`
* If a match is found, calculate candidate `e = e1+e2`, then if `a == g^e mod p` we give `e` to the server

This works because the logarithms "meet in the middle" at `m`. Since the algorithm is probabilistic, we are not guaranteed to find a solution, but with a little bit of luck (And a lot of time waiting, took an hour or two) we finally got the flag `SECT{SHUT_UP_4ND_T4K3_MY_FL4G!!!}`
