#include <string.h>
#include <stdio.h>

typedef unsigned int uint;

char* my_strstr(const char *s1, const char *s2) {
    uint i = 0;
    uint j = 0;

    while (s1[i]) {
        if (j > 0 && s2[j] == '\0') return (char*) s1 + i - j;

        if (s1[i] == s2[j]) j++;
        else j = 0;
        ++i;

        printf("i %d j %d %c %c\n", i, j, s1[i], s2[j]);
    }

    printf("j %d %c\n", j, s2[j]);
    if (j > 0 && s2[j] == '\0') {
        puts("babar");
        return (char*) s1 + i - j;
    }

    return NULL;
}

int my_strncmp(const char *s1, const char *s2, uint L) {
    uint i = 0;

    while (s1[i] && s2[i] && i < L) {
        if (s1[i] != s2[i]) break;
        i++;
    }
    
    return !(i == L);
}

char* my_strstr_lame(const char *s1, const char *s2) {
    uint j = 0;
    uint L = 0;
    while (s2[L]) L++; // strlen(s2);

    for (uint i = 0; s1[i]; i++) {
        if (my_strncmp(s1 + i, s2, L) == 0) {
            return (char*) s1 + i;
        }
    }

    return NULL;
}

#define STRSTR my_strstr_lame

int main() {
    {
        const char *largestring = "Foo Bar Baz";
        const char *smallstring = "Bar";
        char *ptr;

        ptr = STRSTR(largestring, smallstring);
        puts(ptr);
    }

    {
        const char *largestring = "bbbc";
        const char *smallstring = "bbc";
        char *ptr;

        ptr = STRSTR(largestring, smallstring);
        puts(ptr);
    }

    return 0;
}
