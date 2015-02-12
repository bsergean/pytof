#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <zlib.h>
#include <pthread.h>

// No STL include -> faster compile !!!
//
// TOO
// * buffer overflow
// * error checking

static const int max_path = 1024;
typedef unsigned char byte;
typedef struct eclair_entry { 
    char f[max_path];
    unsigned long len_uncompressed;
    unsigned long len_compressed;
    unsigned long offset;
    int id;
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

    unsigned long offset = header.data_offset;
    for (int i = 0; i < header.file_count; ++i) {

        eclair_entry entry = header.entries[i];
        entry.offset = offset;
        printf("%s %zu %zu %zu\n", entry.f, 
               entry.len_compressed, entry.len_uncompressed,
               entry.offset);

        offset += entry.len_compressed;
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
    inflate_read_data(fn, header, true);
    puts("inflate_read done");
}

void inflate_mmap_read_data(char* fn, 
    eclair_header& header, bool write_to_disk = true) {
    int fd = open(fn, O_RDONLY, 0);
    if (fd == -1) return;
    struct stat st;
    if (fstat(fd, &st) != 0) return;
    long len = st.st_size;
    
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

    for (int i = 0; i < header.file_count; ++i) {

        eclair_entry entry = header.entries[i];
        puts(entry.f);

        byte* uncompressed = new byte[entry.len_uncompressed];

        // decompress
        uncompress(uncompressed, &entry.len_uncompressed,
                   buf + entry.offset, entry.len_compressed);

        if (write_to_disk) {
            // write to a new file
            FILE* fw = fopen(entry.f, "w");
            fwrite(uncompressed, sizeof(byte), 
                   entry.len_uncompressed, fw);
            fclose(fw);
        }
        
        delete [] uncompressed;
    }

    munmap(buf, len);
}

void inflate_mmap(char* fn) {
    eclair_header header;
    inflate_read_header(fn, header);
    inflate_mmap_read_data(fn, header, true);
    puts("inflate_mmap done");
}

byte* g_buf;
void* decompress(void *fn_void) {
    eclair_entry entry = *((eclair_entry*) fn_void);
    printf("%d %s %p\n", entry.id, entry.f, pthread_self());

    byte* uncompressed = new byte[entry.len_uncompressed];

    // decompress
    uncompress(uncompressed, &entry.len_uncompressed,
               g_buf + entry.offset, entry.len_compressed);

    bool write_to_disk = true;
    if (write_to_disk) {
        // write to a new file
        FILE* fw = fopen(entry.f, "w");
        fwrite(uncompressed, sizeof(byte), 
                entry.len_uncompressed, fw);
        fclose(fw);
    }

    delete [] uncompressed;
}

void inflate_mmap_threaded_read_data(char* fn, 
    eclair_header& header, bool write_to_disk = true) {
    int fd = open(fn, O_RDONLY, 0);
    if (fd == -1) return;
    struct stat st;
    if (fstat(fd, &st) != 0) return;
    long len = st.st_size;
    
    g_buf = (byte*) mmap((caddr_t) 0, len, PROT_READ, 
                         MAP_PRIVATE, fd, 0);
    if (g_buf == MAP_FAILED) {
        puts("map failed"); 
        return;
    }
    int ret = madvise (g_buf, len, MADV_RANDOM);
    if (ret < 0) {
        puts("madvise failed"); 
        return;
    }

    pthread_t threads[header.file_count];
    void *status;

    for (int i = 0; i < header.file_count; ++i) {
        eclair_entry entry = header.entries[i];
        entry.id = i;

        ret = pthread_create(&threads[i], NULL, 
                             decompress, (void *) &entry);
        if (ret){
            printf("ERROR; return code from pthread_create()"
                   " is %d\n", ret);
            exit(-1);
        }
    }

    // Join
    for (int i = 0; i < header.file_count; ++i) {
        ret = pthread_join(threads[i], &status);
        if (ret){
            printf("ERROR; return code from pthread_join() is %d\n", 
                   ret);
            exit(-1);
        }
    }

    pthread_exit(NULL);
    munmap(g_buf, len);
}

void inflate_mmap_threaded(char* fn) {
    eclair_header header;
    inflate_read_header(fn, header);
    inflate_mmap_threaded_read_data(fn, header, false);
    puts("inflate_mmap_threaded done");
}
int main(int argc, char** argv) {
    if (argc == 2) {
        inflate(argv[1]);
    }
    if (argc == 3) {
        inflate_mmap(argv[1]);
    }
    if (argc == 4) {
        inflate_mmap_threaded(argv[1]);
    }
}
