#include <vector>
#include <iostream>
#include <stdint.h>

long long
factorial(long long n)
{
    long long ret = 1;
    while (n > 1) {
        n--;
        ret *= n;
    }
    return ret;
}

int
trailingZeroes(int n)
{
    long long x = factorial(n);
    int count = 0;
    do {
        if ((x % 10) != 0) {
            break;
        } else {
            count++;
            x /= 10;
        }
    } while (x != 0);

    return count;
}

int
trailingZeroes2(int n)
{
    int count = 0;
    for (int i = 0; i < n; i += 5) {
        if (i == 0) continue;

        int j = 5;
        while (j < n) {
            if (i % j == 0) {
                count += 1;
            }
            j *= 5;
        }
    }

    return count;
}

int
trailingZeroes3(int n)
{
    int count = 0;

    int j = 5;
    while (j < n) {
        count += n / j;
        j *= 5;
    }

    return count;
}

int
trailingZeroes4(int n)
{
//    if (n < 5) return 0;
//    if (n == 5) return 1;

    uint64_t count = 0;
    uint64_t N = n;

    uint64_t j = 5;
    while (j < N) {
        count += N / j;
        j *= 5;
    }

    return (int) count;
}

int
main()
{
    for (uint64_t N = 1; N < 1000; ++N) {
        std::cout << "trailingZeroes " << N << " -> " 
                  << trailingZeroes4(N) << std::endl;
    }
}

