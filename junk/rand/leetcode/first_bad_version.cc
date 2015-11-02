#include <iostream>

bool 
isBadVersion(int version)
{
    return version >= 1;
}

int 
firstBadVersion(int n) 
{
    int lo = 0;
    int hi = n - 1;

    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;

        bool badVersion = isBadVersion(mid);
        if (badVersion) {
            if (!isBadVersion(mid - 1)) {
                return mid;
            } else {
                hi = mid - 1;
            }
        } else {
            lo = mid + 1;
        }
    }

    return n;
}

int 
main()
{
    std::cout << firstBadVersion(10) << std::endl;

    return 0;
}
