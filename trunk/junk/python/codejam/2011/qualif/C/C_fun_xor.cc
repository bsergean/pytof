#include <iostream>
#include <vector>
#include <string>
#include <list>
using namespace std;
typedef unsigned int uint;

const uint B0  = 1 << 0;
const uint B1  = 1 << 1;
const uint B2  = 1 << 2;
const uint B3  = 1 << 3;
const uint B4  = 1 << 4;
const uint B5  = 1 << 5;
const uint B6  = 1 << 6;
const uint B7  = 1 << 7;
const uint B8  = 1 << 8;
const uint B9  = 1 << 9;
const uint B10 = 1 << 10;
const uint B11 = 1 << 11;
const uint B12 = 1 << 12;
const uint B13 = 1 << 13;
const uint B14 = 1 << 14;
const uint B15 = 1 << 15;
const uint B16 = 1 << 16;
const uint B17 = 1 << 17;
const uint B18 = 1 << 18;
const uint B19 = 1 << 19;
const uint B20 = 1 << 20;
const uint B21 = 1 << 21;
const uint B22 = 1 << 22;
const uint B23 = 1 << 23;
const uint B24 = 1 << 24;
const uint B25 = 1 << 25;
const uint B26 = 1 << 26;
const uint B27 = 1 << 27;
const uint B28 = 1 << 28;
const uint B29 = 1 << 29;
const uint B30 = 1 << 30;
const uint B31 = 1 << 31;

void printBinary(uint a)
{
    string s;

    if (a & B31) s += "1"; else s += "0";
    if (a & B30) s += "1"; else s += "0";
    if (a & B29) s += "1"; else s += "0";
    if (a & B28) s += "1"; else s += "0";
    if (a & B27) s += "1"; else s += "0";
    if (a & B26) s += "1"; else s += "0";
    if (a & B25) s += "1"; else s += "0";
    if (a & B24) s += "1"; else s += "0";
    if (a & B23) s += "1"; else s += "0";
    if (a & B22) s += "1"; else s += "0";
    if (a & B21) s += "1"; else s += "0";
    if (a & B20) s += "1"; else s += "0";
    if (a & B19) s += "1"; else s += "0";
    if (a & B18) s += "1"; else s += "0";
    if (a & B17) s += "1"; else s += "0";
    if (a & B16) s += "1"; else s += "0";
    if (a & B15) s += "1"; else s += "0";
    if (a & B14) s += "1"; else s += "0";
    if (a & B13) s += "1"; else s += "0";
    if (a & B12) s += "1"; else s += "0";
    if (a & B11) s += "1"; else s += "0";
    if (a & B10) s += "1"; else s += "0";
    if (a & B9)  s += "1"; else s += "0";
    if (a & B8)  s += "1"; else s += "0";
    if (a & B7)  s += "1"; else s += "0";
    if (a & B6)  s += "1"; else s += "0";
    if (a & B5)  s += "1"; else s += "0";
    if (a & B4)  s += "1"; else s += "0";
    if (a & B3)  s += "1"; else s += "0";
    if (a & B2)  s += "1"; else s += "0";
    if (a & B1)  s += "1"; else s += "0";
    if (a & B0)  s += "1"; else s += "0";
    
    cout << a << " in binary is " << s << endl;
}

uint addBinary(uint a, uint b)
{
    uint out = 0;

    if ( (a & B0) != (b & B0) ) out += B0;
    if ( (a & B1) != (b & B1) ) out += B1;
    if ( (a & B2) != (b & B2) ) out += B2;
    if ( (a & B3) != (b & B3) ) out += B3;
    if ( (a & B4) != (b & B4) ) out += B4;
    if ( (a & B5) != (b & B5) ) out += B5;
    if ( (a & B6) != (b & B6) ) out += B6;
    if ( (a & B7) != (b & B7) ) out += B7;
    if ( (a & B8) != (b & B8) ) out += B8;
    if ( (a & B9) != (b & B9) ) out += B9;
    if ( (a & B10) != (b & B10) ) out += B10;
    if ( (a & B11) != (b & B11) ) out += B11;
    if ( (a & B12) != (b & B12) ) out += B12;
    if ( (a & B13) != (b & B13) ) out += B13;
    if ( (a & B14) != (b & B14) ) out += B14;
    if ( (a & B15) != (b & B15) ) out += B15;
    if ( (a & B16) != (b & B16) ) out += B16;
    if ( (a & B17) != (b & B17) ) out += B17;
    if ( (a & B18) != (b & B18) ) out += B18;
    if ( (a & B19) != (b & B19) ) out += B19;
    if ( (a & B20) != (b & B20) ) out += B20;
    if ( (a & B21) != (b & B21) ) out += B21;
    if ( (a & B22) != (b & B22) ) out += B22;
    if ( (a & B23) != (b & B23) ) out += B23;
    if ( (a & B24) != (b & B24) ) out += B24;
    if ( (a & B25) != (b & B25) ) out += B25;
    if ( (a & B26) != (b & B26) ) out += B26;
    if ( (a & B27) != (b & B27) ) out += B27;
    if ( (a & B28) != (b & B28) ) out += B28;
    if ( (a & B29) != (b & B29) ) out += B29;
    if ( (a & B30) != (b & B30) ) out += B30;
    if ( (a & B31) != (b & B31) ) out += B31;
    
    return out;
}

int compute(list<uint>& candies)
{
    L = len(candies)
    winner = -1
    for i in xrange(L):
        for i in xrange(0, L-1):
            A = 0
            realA = 0
            B = 0
            realB = 0
            j = 0
            while j <= i:
                A = addBin(A, candies[j])
                realA += candies[j]
                j += 1

            k = L - 1
            while k > i:
                B = addBin(B, candies[k])
                realB += candies[k]
                k -= 1

            if A == B:
                candidate = max(realA, realB)
                if candidate > winner:
                    winner = candidate
                
        candies.rotate()

    if winner == -1: return 'NO'
    else: return winner
}

int main()
{
    printBinary(12345);

    printBinary(12);
    printBinary(5);

    printBinary(B3);
    printBinary(B2);
    printBinary(B1);
    printBinary(B0);

    printf("%d\n", 12 & B3);
    printf("%d\n", 5 & B3);
    printf("%d\n", (5 & B3) != (12 & B3));

    printf("xor - %d\n", 12 ^ 5);

    uint ret = addBinary(12, 5); // shoudl be 9
    cout << "Ret " << ret << endl;

    uint A;
    cin >> A;
    cout << "You entered " << A << endl;
}
