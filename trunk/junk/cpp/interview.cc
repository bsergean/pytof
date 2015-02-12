#include <stdio.h>
#include <string.h>

void
removeChar(char* s, char c)
{
    int j = 0;
    for (int i = 0, N = strlen(s); i < N; ++i) {
        if (s[i] != c) {
            s[j] = s[i];
            j++;
        }
    }
    s[j] = '\0';
}

int
main()
{
    char s[] = "google";
    size_t len = strlen(s);

    printf("%s\n", s);

    removeChar(s, 'o');

    printf("%s\n", s);

    return 0;
}
