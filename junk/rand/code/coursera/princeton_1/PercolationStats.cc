#include "PercolationStats.h"
#include "Percolation.h"
#include <stdlib.h>
#include <iostream>

namespace {
int
randInt(int N)
{
    // return (int) rand() % N;
    return ((double) rand() / (double) RAND_MAX) * N;
}

#if 0
void
randInt(int& i, int& j, int N)
{
    int ret = (int) rand() % (N*N);
}
#endif

}

PercolationStats::PercolationStats(int N, int T)
{
    srand(time(NULL));

    mMean = 0;
    double mean = 0;

    for (uint i = 0; i < T; ++i) {
        std::cout << "Test " << i << std::endl << std::endl;

        Percolation percolation(N);
        uint j = 0;
        do {
            int iRand = randInt(N);
            int jRand = randInt(N);

            if (!percolation.isOpen(iRand, jRand)) {
                percolation.open(iRand, jRand);
                j++;

                std::cout << j << std::endl;
                percolation.print();
            }

        } while (!percolation.percolates());

        std::cout << j << std::endl;
        mean += (double) j / (N*N);
    }

    mMean = mean / T;
}

double 
PercolationStats::mean() const
{
    return mMean;
}

double 
PercolationStats::stddev()
{
    return 0;
}

double 
PercolationStats::confidenceLo()
{
    return 0;
}

double 
PercolationStats::confidenceHi() 
{
    return 0;
}
