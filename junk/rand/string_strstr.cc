#include <stdio.h>
#include <string.h>

namespace rand {

int
strncmp(char* haystack, char* needle, int N)
{
    if (haystack == NULL || needle == NULL) { 
        return false;
    }

    for (int i = 0; i < N; ++i) {
        if (haystack[i] != needle[i]) {
            return false;
        }
    }

    return true;
}

char*
strstr(char* haystack, char* needle)
{
    int M = strlen(haystack);
    int N = strlen(needle);
    int steps = M - N + 1;

    for (int i = 0; i < steps; ++i) {
        if (rand::strncmp(haystack + i, needle, N)) {
            return haystack + i;
        }
    }

    return NULL;
}

} // end namespace

int
main()
{
    char haystack[] = "googleeuh";
    char needle  [] = "et";

    printf("strstr(\"%s\", \"%s\") = %s\n", 
           haystack, needle, rand::strstr(haystack, needle));

    return 0;
}
