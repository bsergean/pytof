#include <stdio.h>
#include <string.h>

int main()
{
    int BUFFER_SIZE = 1 << 15;
    char bufferIn[BUFFER_SIZE];

    do {
        // READ from stdin
        int count = read(0, bufferIn, BUFFER_SIZE);
        if (count <= 0) break;
        write(1, bufferIn, BUFFER_SIZE);
    } while (1);
}

