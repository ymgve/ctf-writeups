# babyuse - exploitation

> nc 202.112.51.247 3456
>
> [Download Attachments](./e1b84982-14dc-45f3-a41b-fb80b4805bd1.zip)

The basics of this exploit is [better covered by another team's writeup](https://github.com/Kileak/CTF/blob/master/2017/bctf/pwn/babyuse/readme.md),
but my solution is similar:

* Create two guns (with long name sizes)
* Select gun0
* Drop gun0
* Use gun0

This gives me an address leak, since the `free()` when you drop the gun adds
the chunk to the linked list of free chunks. Now, changing the name of gun1 to
a 15 character long name will re-use the structure of gun0, which gives me an
arbitrary memory leak, and also an arbitrary vtable pointer. Need to do a bit
more leaking - first leak was to the libc `main_arena` structure, and right
below the address we leaked is the address to a chunk on the heap. After this,
it's relatively easy to get EIP control by adding another gun which contains a
fake vtable in the name - placed at a predictable point of the heap, and then
rename gun1 twice to set a pointer to the vtable.

But where to jump? Unlike the guys in the previously linked writeup, I couldn't
get an one-shot shell call to work, and had a hard time finding a good
solution. It's easy enough to call `system()` in libc, but the first parameter
is the gun object, and at the start of that object is a pointer to a vtable,
not an usable string.

_Unless_...it can be both! If I somehow manage to point to a valid vtable
containing the address of `system()` at an address like `??006873`, it will
be seen as the string `"sh"` by the `system()` call, which then should give me
a shell. So, the solution becomes:

* Create a gun with a _huge_ (16MB) name, filled with the address of `system()`, offset by 3 bytes
* Leak the address of this name (Only really need the upper 8 bits) and set `XX006873` as the vtable for gun0
* Fire gun0

This worked perfectly when I tested it locally, but sending 16MB of data was
too much for the competition system, so I reduced the amount of data I sent -
this reduced the chance of the exploit working, but that was just a matter of
running the exploit multiple times. After a few runs I got lucky, and got the
flag.
