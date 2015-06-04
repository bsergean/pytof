#include <set>
#include <iostream>

int
next(int x)
{
    int sum = 0;

    do {
        int lastDigit = x % 10;
        sum += lastDigit * lastDigit;
        x /= 10;
    } while (x != 0);

    return sum;
}

bool
happy(int n)
{
    std::set<int> numbers;
    int x = n;

    for (;;) {
        x = next(x);
        if (x == 1) return true;
        if (numbers.count(x) > 0) return false;
    }
}

int
main()
{
    std::cout << next(19) << std::endl;
    std::cout << happy(19) << std::endl;
}
