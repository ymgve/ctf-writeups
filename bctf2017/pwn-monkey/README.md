# monkey - exploitation

> nc 202.112.51.248 2333
>
> http://ftp.mozilla.org/pub/firefox/nightly/2016/07/2016-07-31-03-02-03-mozilla-central/jsshell-linux-x86_64.zip

So, we got a link to a Javascript shell - straight from Mozilla's servers. At
first I thought we had to use an exploit that was later fixed, since the
linked build is almost a year old. But after looking through the changelog and
finding nothing interesting, I started exploring what capabilites are built
into the shell.

The [list of built in functions](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey/Introduction_to_the_JavaScript_shell)
seemed pretty unhelpful apart from the `read()` function, but without some way
to navigate the file system I was stuck. Spent some time looking around the
[shell source code](https://dxr.mozilla.org/mozilla-central/source/js/src/shell/js.cpp)
until I searched globally for `JSFunctionSpecWithHelp` to find other functions
that might possibly help, and saw that there was a separate `os` namespace,
which also included `os.system()`!

Not sure if this was the intended way to solve the challenge, but with full
access to shell commands it was easy to locate and grab the flag.
