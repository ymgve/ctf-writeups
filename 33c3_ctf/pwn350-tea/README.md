# Tea - Exploitation - 350 points

> `nc 104.155.105.0 14000`
> tea
> environment: `docker run -i -t tsuro/nsjail-ctf /bin/bash`

We're given a binary that allows us to repeatedly read the content of files on the target machine. It first maps a huge
memory space, picks a random point inside that memory space, then uses `clone()` with that address as the child process
stack area.

The child sets up a SECCOMP filter. Using `scmp_bpf_disasm.c` in the
[SECCOMP github](https://github.com/seccomp/libseccomp/tree/master/tools) repo, we disassemble the filter and find it allows the `exit`, `exit_group`, `brk`, `mmap`, `read`, `lseek`, `open`, `close` and `write` system calls, but `mmap` only
allows you to allocate RW memory, `close` disallows closing file descriptors 0, 1 and 2 (stdin, stdout and stderr) and
`write` only allows writing to file descriptors 1 and 2. (stdout and stderr) 

The code for the child process function - it's basically a loop that reads filename, offset and buffer size, then sends the
read data to stdout:

    void __fastcall __noreturn fn(void *arg)
    {
      unsigned __int64 seek_offset; // rax@8
      int count; // eax@9
      int count_; // eax@11
      char input; // [sp+10h] [bp-40h]@2
      char input_end; // [sp+2Fh] [bp-21h]@2
      size_t n; // [sp+38h] [bp-18h]@11
      int fd; // [sp+40h] [bp-10h]@3
      int oflag; // [sp+44h] [bp-Ch]@3
      void *buf; // [sp+48h] [bp-8h]@8

      setup_seccomp();
      while ( 1 )
      {
        puts("(r)ead or (w)rite access?");
        gets(&input);
        input_end = 0;
        if ( input != 'r' )
          break;
        oflag = 0;
        puts("filename?");
        gets(&input);
        input_end = 0;
        fd = open(&input, oflag);
        if ( fd < 0 )
          err(1, "open(%s)", &input);
        puts("lseek?");
        gets(&input);
        input_end = 0;
        seek_offset = strtoull(&input, 0LL, 10);
        lseek(fd, seek_offset, 0);
        puts("count?");
        buf = &input;
        gets(&input);
        input_end = 0;
        if ( atoi(&input) > 0x20 )
        {
          count = atoi(&input);
          buf = malloc(count);
          if ( !buf )
            err(1, "malloc");
        }
        count_ = atoi(&input);
        n = read(fd, buf, count_ - 1);
        if ( (n & 0x8000000000000000LL) != 0LL )
          err(1, "read");
        printf("read %d bytes\n", n);
        write(1, buf, n);
        close(fd);
        puts("quit? (y/n)");
        read(0, &input, 2uLL);
        if ( input != 'n' )
          exit(0);
      }
      puts("write mode not supported in the trial, please upgrade your plan by sending 10 BTC to tsuro.");
      exit(1);
    }

We first note that there are multiple buffer overflows in the way the inner loop reads the filename, offset and size as it
uses `gets()`, but since the function never returns, only uses `exit()`, simply overwriting the return address gets us
nowhere.

But there are a few things we can do with an overflow - consider the code for getting how many bytes to read:

        puts("count?");
        buf = &input;
        gets(&input);
        input_end = 0;
        if ( atoi(&input) > 0x20 )
        {
          count = atoi(&input);
          buf = malloc(count);
          if ( !buf )
            err(1, "malloc");
        }
    
The buffer used for reading input is re-used as the buffer for reading file data if the size is 32 bytes or less. As you
can see, `buf` gets set *before* it reads the size, which means overflowing allows us to set the destination buffer to
wherever we want to in memory. This overflow also allows us to set a different file descriptor for the `read()` and
`close()` calls. But still, how do we take control over RIP and get a shell?

We have full file system read access - so what can we do with that? First of all, there's `/proc/self/maps`. Parsing the
content of this file gives us the stack address of the **parent** process, and the address of libc and the binary itself.
We also read `/proc/self/status` to get the parent PID.

And then there's `/proc/self/mem`. Combined with the `fseek()` offset, this allows us to dump anything in the process
memory. We use this to get the actual libc binary for later use. We also know the stack address of the parent process, and
since it used `clone()` instead of `fork()`, a copy of the parent stack at call time is still present in the child process
memory space. Reading the parent stack allows us to find the random value used for setting the child stack, and we then
know the position of the child stack too.

While the main loop never uses `ret`, the library calls of course do. We can set read size to
-2147483648, which is below 32 so no memory is allocated. We set the file descriptor to stdin, and set the buffer
destination to where the return address will be when inside the `read()` function. We now have RIP control, and can upload
an arbitrary size ROP chain.

Still only halfway though. Remember SECCOMP? `execve` is disallowed, so we can't call `system()`. But - the **parent**
process doesn't have any such restrictions - how can we take control over it?

Our plan: Use `/proc/[parentPID]/mem` to overwrite a return address there. The parent process is still inside `waitpid()`
waiting for the child to finish, so it should be easy enough if we get write access to that file. But how? SECCOMP only
allows us to write to fd 1 and 2. If we could close stderr, then a newly opened file would get assigned to fd 2, but as
previously mentioned, it blocks closing file descriptors 0-2. We can't close fd 2.

*But what about file descriptor `0x8000000000000002`?*

Surprisingly enough, it works! SECCOMP allows this to go through since it's clearly not 0, 1, nor 2, and somewhere the libc
and/or kernel decides to ignore the topmost bit we set. We can now open `/proc/[parentPID]/mem` in read+write mode, it gets
assigned to fd 2, and we can overwrite the return from `waitpid()` with a second stage ROP chain that calls `system()`. 

After a short exploration with `/bin/sh` we find the setuid binary `/home/user/getflag`, and running it finally rewards us 
with the flag `33C3_why_do_y0u_3ven_filter?!?`