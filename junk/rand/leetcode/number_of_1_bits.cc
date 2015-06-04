#include <iostream>
#include <stdint.h>

//
// todo: table based solution
//
int 
hammingWeight(uint32_t n) 
{
    int sum = 0;
    for (int i = 0; i < 32; ++i) {
        if (n & (1 << i)) {
            sum++;
        }
    }
    return sum;
}

//
// the 32-bit integer ’11' has binary representation 00000000000000000000000000001011, so the function should return 3.
//
int main()
{
    int N = 11;
    std::cout << N << " -> " << hammingWeight(N) << std::endl;
}
