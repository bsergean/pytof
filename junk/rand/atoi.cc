#include <stdio.h>
#include <string.h>

// only works for positive integers
int
char2digit(char c)
{
    switch (c) {
        case '0': return 0;
        case '1': return 1;
        case '2': return 2;
        case '3': return 3;
        case '4': return 4;
        case '5': return 5;
        case '6': return 6;
        case '7': return 7;
        case '8': return 8;
        case '9': return 9;
        default: return -1;
    }
}

int
aToi(const char* str)
{
    if (str == NULL) { return -1; }

    int result = 0;
    int N = strlen(str);
    int units = 1;

    for (int i = 0; i < N; ++i) {
        int idx = N - i - 1;

        int digit = char2digit(str[idx]);
        if (digit < 0) return -1;

        result += (units * digit);
        units *= 10;
    }

    return result;
}

int 
main()
{
    printf("char2digit[%c] = %d\n", '0', char2digit('0'));
    printf("char2digit[%c] = %d\n", '3', char2digit('3'));
    printf("char2digit[%c] = %d\n", '9', char2digit('9'));
    printf("char2digit[%c] = %d\n", 'A', char2digit('A'));

    const char* s1 = "123";
    printf("atoi[%s] = %d\n", s1, aToi(s1));
}
