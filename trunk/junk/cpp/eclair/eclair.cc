#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <zlib.h>

// No STL include -> faster compile !!!
//
// TOO
// * buffer overflow
// * error checking

static const int max_path = 1024;
typedef struct eclair_entry { 
    char f[max_path];
    unsigned long len_uncompressed;
    unsigned long len_compressed;
};
typedef struct eclair_header { 
    eclair_entry* entries;
    long file_count;
    long data_offset;
};

void inflate_read_header(char* fn, eclair_header& header) {
    FILE* fo = fopen(fn, "r");
    if (fo == NULL) return;

    char buf[max_path];
    char* end;

    fgets(buf, sizeof(buf), fo);
    long file_count = strtol(buf, &end, 10);
    header.entries = new eclair_entry[file_count];

    for (int i = 0; i < file_count; ++i) {

        eclair_entry entry;
        fgets(buf, sizeof(buf), fo);
        strcpy(entry.f, buf);
        // discard the trailing \n
        entry.f[ strlen(entry.f)-1 ] = '\0';

        fgets(buf, sizeof(buf), fo);
        entry.len_uncompressed = strtoul(buf, &end, 10);

        fgets(buf, sizeof(buf), fo);
        entry.len_compressed = strtoul(buf, &end, 10);

        header.entries[i] = entry;
    }

    header.file_count = file_count;
    header.data_offset = ftell(fo);

    fclose(fo);

    for (int i = 0; i < header.file_count; ++i) {

        eclair_entry entry = header.entries[i];
        printf("%s %zu %zu\n", entry.f, 
               entry.len_compressed, entry.len_uncompressed);
    }
}

void inflate_read_data(char* fn, 
    eclair_header& header, bool write_to_disk = true) {
    FILE* fo = fopen(fn, "r");
    if (fo == NULL) return;

    fseek(fo, header.data_offset, SEEK_SET);

    for (int i = 0; i < header.file_count; ++i) {

        eclair_entry entry = header.entries[i];
        puts(entry.f);

        typedef unsigned char byte;
        byte* compressed = new byte[entry.len_compressed];
        byte* uncompressed = new byte[entry.len_uncompressed];

        // read from disk
        fread(compressed, sizeof(byte), 
              entry.len_compressed, fo);

        // decompress
        uncompress(uncompressed, &entry.len_uncompressed,
                   compressed, entry.len_compressed);

        if (write_to_disk) {
            // write to a new file
            FILE* fw = fopen(entry.f, "w");
            fwrite(uncompressed, sizeof(byte), 
                    entry.len_uncompressed, fw);
            fclose(fw);
        }
        
        delete [] compressed;
        delete [] uncompressed;
    }

    fclose(fo);
}

void inflate(char* fn) {
    eclair_header header;
    inflate_read_header(fn, header);
    inflate_read_data(fn, header, false);
    puts("inflate_read done");
}

void inflate_mmap_read_data(char* fn, 
    eclair_header& header, bool write_to_disk = true) {
    int fd = open(fn, O_RDONLY, 0);
    if (fd == -1) return;
    struct stat st;
    if (fstat(fd, &st) != 0) return;
    long len = st.st_size;
    
    typedef unsigned char byte;
    byte* buf = (byte*) mmap((caddr_t) 0, len, PROT_READ, 
                             MAP_PRIVATE, fd, 0);
    if (buf == MAP_FAILED) {
        puts("map failed"); 
        return;
    }
    int ret = madvise (buf, len, MADV_SEQUENTIAL);
    if (ret < 0) {
        puts("madvise failed"); 
        return;
    }

    long offset = header.data_offset;
    for (int i = 0; i < header.file_count; ++i) {

        eclair_entry entry = header.entries[i];
        puts(entry.f);

        byte* uncompressed = new byte[entry.len_uncompressed];

        // decompress
        uncompress(uncompressed, &entry.len_uncompressed,
                   buf + offset, entry.len_compressed);

        if (write_to_disk) {
            // write to a new file
            FILE* fw = fopen(entry.f, "w");
            fwrite(uncompressed, sizeof(byte), 
                   entry.len_uncompressed, fw);
            fclose(fw);
        }
        
        delete [] uncompressed;

        offset += entry.len_compressed;
    }

    munmap(buf, len);
}

void inflate_mmap(char* fn) {
    eclair_header header;
    inflate_read_header(fn, header);
    inflate_mmap_read_data(fn, header, false);
    puts("inflate_mmap done");
}

int main(int argc, char** argv) {
    if (argc == 2) {
        inflate(argv[1]);
    }
    if (argc == 3) {
        inflate_mmap(argv[1]);
    }
}
