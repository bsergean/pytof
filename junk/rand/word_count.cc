#include <cassert>
#include <cstring>
#include <stdio.h>

int
wcScan(const char* str)
{
    if (str == NULL) return 0;

    int count = 0;
    int i = 0;
    int N = strlen(str);

    if (N == 0) return 0;

    for (;;) {

        while (i != N && str[i++] == ' ');
        if (i == N) break;

        count++;

        while (i != N && str[i++] != ' ');
        if (i == N) break;
    }

    return count;
}

int
wcState(const char* str)
{
    if (str == NULL) return 0;

    int count = 0;
    int i = 0;
    int N = strlen(str);

    if (N == 0) return 0;

    bool space = str[0] == ' ';
    if (!space) { count++; }

    for (i = 0; i < N; ++i) {
        bool isSpace = str[i] == ' ';
        bool stateChange = (space != isSpace);

        if (stateChange && !isSpace) {
            count++;
        }
        space = isSpace;
    }

    return count;
}

int
wcPipe(const char* str)
{
    if (str == NULL) return 0;

    char command[128];
    sprintf(command, "echo '%s' | wc -w", str);
    
    FILE* stream = popen(command, "r");
    int count = 0;
    char buffer[128];
    fgets(buffer, 128, stream);

    sscanf(buffer, "%d", &count);
    pclose(stream);

    printf("'%s' -> %d\n", str, count);

    return count;
}

int
wc(const char* str)
{
    // return wcState(str);
    // return wcScan(str);
    return wcPipe(str);
}

int
main()
{
    assert(wc(NULL) == 0);
    assert(wc("") == 0);

    assert(wc(" ") == 0);
    assert(wc("  ") == 0);

    assert(wc(" un") == 1);
    assert(wc("  un") == 1);
    assert(wc("un ") == 1);
    assert(wc("un  ") == 1);
    assert(wc(" un ") == 1);
    assert(wc("  un ") == 1);
    assert(wc("  un  ") == 1);

    assert(wc("un deux  ") == 2);
    assert(wc(" un deux  ") == 2);
    assert(wc(" un deux") == 2);
    assert(wc("un deux trois") == 3);
}




