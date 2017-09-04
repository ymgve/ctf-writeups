import ctypes

libc = ctypes.CDLL('libc.so.6')
seccomp = ctypes.CDLL('libseccomp.so.2')

SCMP_ACT_KILL       = 0x00000000
SCMP_ACT_TRAP       = 0x00030000
SCMP_ACT_ERRNO_0    = 0x00050000
SCMP_ACT_ALLOW      = 0x7fff0000


class Restrict(object):
    def set_timeout(self, n=10):
        libc.alarm(n)

    def seccomp(self):
        ctx = seccomp.seccomp_init(SCMP_ACT_ERRNO_0)
        ret = 0
        ret |= seccomp.seccomp_rule_add(ctx, SCMP_ACT_ALLOW, 1, 0) # allow write
        ret |= seccomp.seccomp_rule_add(ctx, SCMP_ACT_ALLOW, 60, 0) # allow exit 
        ret |= seccomp.seccomp_rule_add(ctx, SCMP_ACT_ALLOW, 3, 0) # allow close
        ret |= seccomp.seccomp_rule_add(ctx, SCMP_ACT_ALLOW, 12, 0) # allow brk 
        ret |= seccomp.seccomp_rule_add(ctx, SCMP_ACT_ALLOW, 10, 0) # allow mprotect
        ret |= seccomp.seccomp_rule_add(ctx, SCMP_ACT_ALLOW, 9, 0) # allow mmap 
        ret |= seccomp.seccomp_rule_add(ctx, SCMP_ACT_ALLOW, 11, 0) # allow munmap
        ret |= seccomp.seccomp_load(ctx)

        assert ret == 0, "Failed to setup syscall."
