
#include <iostream>
#include <stdint.h>

uint32_t 
reverseBits(uint32_t n) 
{
    int out = 0;

    for (int i = 0; i < 32; ++i) {
        if (n & (1 << i)) {
            // set inverse bit to 1
            out |= (1 << (32 - i - 1));
        }
    }

    return out;
}

//
// For example, given input 43261596 (represented in binary as 00000010100101000001111010011100), return 964176192 (represented in binary as 00111001011110000010100101000000).
//
int main()
{
    int N = 43261596;
    std::cout << N << " -> " << reverseBits(N) << std::endl;
}
