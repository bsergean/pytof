#include <stdio.h>

/*
int level29()
{
    int S = 0;
    for (int p = 0; p < 1000; p++)
    {
        printf("%d\n",p);
        for (int a = 1; a < p; a++)
            for (int b = a; b < p; b++) 
            {
                float c = sqrt(a*a + b*b);
                if (c < b) continue;
                double fractional;
                float C = modf(c, &fractional);
                if (fractional != 0.0) continue;
                if ((int)(a+b+c) == (int) p) S += 1;
            }
    }

    printf("Res: S = %d\n", S);
}
*/

/* gcc -O4 -std=c99 euler.c -o c_euler */
void level12()
{
    int n = 1;
    int k = 1;

    while (1) {

        k += 1;
        n += k;

        int L = 0;
        int max_int = n / 2 + 1;
        for (int i = 1; i < max_int; i++)
            if (n % i == 0)
                L += 1;
        
        printf("divisors: %-3d triangle-number: %d index: %d\n", L, n, k);
        if (L >= 500) {
            return;
        }
    }
}

int main()
{
    level12();
    /* level29(); */
}
