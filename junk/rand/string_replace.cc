#include <stdio.h>
#include <string.h>

void
replace(char* s)
{
    int N = strlen(s);
    int j = N - 1;

    int P = 0;
    for (int i = (N-1); i > 0; --i) {
        if (s[i] != ' ') { 
            P = i;
            break;
        }
    }

    N = P + 1;

    for (int i = (N-1); i > 0; --i) {

        if (s[i] != ' ') {
            s[j] = s[i];
            j--;
        } else {
            s[j]   = '0';
            s[j-1] = '2';
            s[j-2] = '%';
            j -= 3;
        }
    }
}

int main()
{
    char input[] = "Mr Jo bar team      ";
    printf("%s -> ", input);
    replace(input);
    puts(input);
}
