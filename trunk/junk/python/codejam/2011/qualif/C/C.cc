/*
./CSolver < input_large_real > out && mv out ~/Downloads/answer.txt
./CSolver < input_real > out && mv out ~/Downloads/answer.txt



llvm-g++ -O3 C.cc -o CSolver
llvm-g++ -O3 C.cc && ./a.out < input_real > out && diff out output_real_ok && echo OK
 */

#include <iostream>
#include <vector>
#include <string>
#include <list>
#include <deque>
using namespace std;
typedef unsigned int uint;

int compute(deque<uint>& candies)
{
    uint L = candies.size();
    int winner = -1;
    for (uint z = 0; z < L; ++z) {
        for (uint i = 0; i < (L-1); ++i) {
            uint A = 0;
            uint realA = 0;
            uint B = 0;
            uint realB = 0;
            uint j = 0;

            deque<uint>::const_iterator it  = candies.begin();
            deque<uint>::const_iterator end = candies.end();

            for (; it != end; ++it) {
                uint elem = *it;
                if (j <= i) {
                    A ^= elem;
                    realA += elem;
                    j += 1;
                } else {
                    B ^= elem;
                    realB += elem;
                }
            }

            if (A == B) {
                int candidate = (int) std::max(realA, realB);
                if (candidate > winner) {
                    winner = candidate;
                }
            }
        }
        uint back = candies.back();
        candies.pop_back();
        candies.push_front(back);
    }

    return winner;
}

int main()
{
    uint T;
    cin >> T;
    for (uint c = 0; c < T; ++c) {
        uint N;
        cin >> N;

        deque<uint> candies;
        for (uint i = 0; i < N; ++i) {
            uint candy;
            cin >> candy;
            candies.push_back(candy);
        }
        cout << "Case #" << c+1 << ": ";
        cerr << "Case #" << c+1 << ": ";

        int ret = compute(candies);

        if (ret == -1) cout << "NO";
        else cout << ret;
        cout << endl;

        if (ret == -1) cerr << "NO";
        else cerr << ret;
        cerr << endl;
    }
}
