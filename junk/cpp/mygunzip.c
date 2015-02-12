#include <stdio.h>
#include <string.h>
#include <zlib.h>

static void
zlib_error(z_stream zst, int err, char *msg)
{
    if (zst.msg == Z_NULL)
        printf("Error %d %s", err, msg);
    else
        printf("Error %d %s: %.200s", err, msg, zst.msg);
}

int main()
{
    int err;
    z_stream zst;

    int BUFFER_SIZE = 1 << 15;
    char bufferIn [BUFFER_SIZE];
    char bufferOut[BUFFER_SIZE];

    zst.zalloc    = (alloc_func) Z_NULL;
    zst.zfree     = (free_func)  Z_NULL;
    zst.avail_in  = BUFFER_SIZE;
    zst.avail_out = BUFFER_SIZE; // XXX should be a little more for overshoot case
    zst.next_in   = (Byte *) bufferIn;
    zst.next_out  = (Byte *) bufferOut;
    err = inflateInit2(&zst, 15 + 32);

    switch(err) {
    case(Z_OK):
        break;
    case(Z_MEM_ERROR):
        printf("Out of memory while decompressing data");
        goto error;
    default:
        inflateEnd(&zst);
        zlib_error(zst, err, "while preparing to decompress data");
        goto error;
    }

    do {
        // READ from stdin
        int count = read(0, bufferIn, BUFFER_SIZE);
        if (count < 0) {
            // XXX inflateEnd ?
            printf("Problem reading input\n");
            goto error;
        }
        if (count == 0) break;

	    zst.avail_out = BUFFER_SIZE;
	    zst.next_out  = (Byte *) bufferOut;
            break;
        default:
            inflateEnd(&zst);
            zlib_error(zst, err, "while decompressing data");
            goto error;
        }
    } while (err != Z_STREAM_END);

    err = inflateEnd(&zst);
    if (err != Z_OK) {
        zlib_error(zst, err, "while finishing data decompression");
        goto error;
    }

    // ALL GOOD !
    return 0;

 error:
    printf("Error");
    return 1;
}

