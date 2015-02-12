#include <stdio.h>

int main()
{
/*
 * cat /proc/self/maps 
 * 00400000-00480000 r-xp 00000000 1f:01 911368     /bin/busybox
 * 10000000-10003000 rw-p 00080000 1f:01 911368     /bin/busybox
 * 10003000-1000d000 rwxp 00000000 00:00 0
 * 2aaa8000-2aaae000 r-xp 00000000 1f:01 1518164    /lib/ld-uClibc.so.0
 * 2aaae000-2aaaf000 rw-p 00000000 00:00 0
 * 2aaed000-2aaee000 rw-p 00005000 1f:01 1518164    /lib/ld-uClibc.so.0
 * 2aaee000-2aaf1000 r-xp 00000000 1f:01 1656580    /lib/libcrypt.so.0
 * 2aaf1000-2ab30000 ---p 00003000 00:00 0
 * 2ab30000-2ab31000 rw-p 00002000 1f:01 1656580    /lib/libcrypt.so.0
 * 2ab31000-2ab43000 rw-p 00000000 00:00 0
 * 2ab43000-2ab81000 r-xp 00000000 1f:01 1541936    /lib/libc.so.0
 * 2ab81000-2abc0000 ---p 0003e000 00:00 0
 * 2abc0000-2abc3000 rw-p 0003d000 1f:01 1541936    /lib/libc.so.0
 * 2abc3000-2abc5000 rw-p 00000000 00:00 0
 * 7fff5000-7fff8000 rwxp ffffe000 00:00 0
 * 
 * 242         seq_printf(m, "%08lx-%08lx %c%c%c%c %08llx %02x:%02x %lu %n",
 * 243                         start,
 * 244                         end,
 * 245                         flags & VM_READ ? 'r' : '-',
 * 246                         flags & VM_WRITE ? 'w' : '-',
 * 247                         flags & VM_EXEC ? 'x' : '-',
 * 248                         flags & VM_MAYSHARE ? 's' : 'p',
 * 249                         pgoff,
 * 250                         MAJOR(dev), MINOR(dev), ino, &len);
 */

    if (!freopen("/proc/self/maps", "r", stdin)) {
        return;
    }

    char mapbuf[256];
    
    while (fgets(mapbuf, sizeof mapbuf, stdin)) {

        char flags[32];
        unsigned long start, end;
        unsigned long long file_offset, inode;
        unsigned dev_major, dev_minor;

        char path[100];

        sscanf(mapbuf, "%08lx-%08lx %c%c%c%c %08llx %02x:%02x %lu %n %s",
               &start, &end, flags, &file_offset, &dev_major, &dev_minor, &i, path);
    }
}
