# ????~Impeccable Artifact~ - Exploitation/"Perfection" - 192 points - 72 teams solved

> Overwhelmingly consummate protection
>
> nc 52.192.178.153 31337
>
> [artifact-4c4375825c4a08ae9d14492b34b3bddd.zip](./artifact-4c4375825c4a08ae9d14492b34b3bddd.zip)

The binary allows you to read and write to arbitrary locations in memory, relative to a stack variable, so generating [ROP](https://en.wikipedia.org/wiki/Return-oriented_programming) code is easy enough. It is made a lot harder by a [seccomp](https://en.wikipedia.org/wiki/Seccomp) filter that seems like it disallows any syscalls except `read, write, fstat, lseek, mmap, mprotect, munmap, brk, exit, exit_group`. Most notably, `open` and `execve` are missing. We spent a lot of time trying to see where a flaw might be, but the disassembled filter code seemed watertight. It was not until someone used a different disassembler than the one in [libseccomp](https://github.com/seccomp/libseccomp/tree/master/tools) that we saw the flaw - if `rax == rdx` then any syscall will go through. This wasn't discovered because the libseccomp disassembler is incomplete - it does not support disassembling any code using the `x` register addressing mode. After exploiting this flaw, we got the flag with normal ROP code - `hitcon{why_libseccomp_cheated_me_Q_Q}`
