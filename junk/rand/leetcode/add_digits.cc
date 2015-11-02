#include <iostream>
#include <cassert>

int
addDigits(int num)
{
    int x = num;

    while (true) {

        int sum = 0;

        while (x) {
            int digit = x % 10;
            sum += digit;
            x /= 10;
        }

        if (sum < 10) return sum;
        x = sum;
    }

    return -1;
}

int
main()
{
    int n;

    n = 38;
    int x = addDigits(n);
    std::cout << "addDigits(" << n << ") = " << x << std::endl;
    assert(x == 2);
    return 0;
}
