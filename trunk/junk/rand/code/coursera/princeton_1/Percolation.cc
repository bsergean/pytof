#include "Percolation.h"
#include <iostream>

Percolation::Percolation(int N)
{
    mVec.resize(N*N + 2);
    mSize = N;

    mUf = new WeightedQuickUnionFind(N*N + 2);

    // open all the top and bottom row;
    mTop    = N*N;
    mBottom = N*N + 1;

    for (uint i = 0; i < N; ++i) {
        mUf->Union(mTop, i);
        mUf->Union(mBottom, N*(N-1) + i);
    }
}

void 
Percolation::printPos(std::string msg, int i, int j, int k) const
{
    bool debug = false; // Change this to debug ::open
    if (!debug) return;

    std::cout << msg 
              << " - " << k
              << " ["  << i
              << ", " << j
              << "]" << std::endl;
}

void 
Percolation::open(int i, int j)
{
    int N = mSize;
    int k = N * i + j;
    mVec[k] = true;

    // connect to 4 neighbors
    int a, b;

    // down
    if (k < N*(N-1)) {
        a = k;
        b = k + N;
        if (mVec[b]) {
            mUf->Union(a, b);
            printPos("down ", i, j, k);
        }
    }

    // up
    if (k >= N) {
        a = k - N;
        b = k;
        if (mVec[a]) {
            mUf->Union(a, b);
            printPos("up   ", i, j, k);
        }
    }

    // left
    if (k % N != 0) {
        a = k - 1;
        b = k;
        if (mVec[a]) {
            mUf->Union(a, b);
            printPos("left ", i, j, k);
        }
    }

    // right
    if ((k + 1) % 5 != 0) {
        a = k;
        b = k + 1;
        if (mVec[b]) {
            mUf->Union(a, b);
            printPos("right", i, j, k);
        }
    }
}

bool 
Percolation::isOpen(int i, int j)
{
    int N = mSize;
    int k = N * i + j;

    bool ret = mVec[k];

    const bool debug = false;
    if (debug) {
        std::cout << "isOpen " << i << " " 
                  << j << " -> " << ret << std::endl;
    }

    return ret;
}

bool
Percolation::isFull(int i, int j)
{
    int N = mSize;
    int k = N * i + j;
    return mVec[k] == false;
}

bool 
Percolation::percolates()
{
    return mUf->find(mTop, mBottom);
}

void
Percolation::printToStream(std::stringstream& ss) const
{
    uint N = mSize;

    for (uint i = 0; i < N; ++i) {
        for (uint j = 0; j < N; ++j) {
            ss << mVec[N * i + j] << " ";
        }
        ss << std::endl;
    }
}

void
Percolation::print() const
{
    std::stringstream ss;
    printToStream(ss);
    std::cout << ss.str();
}

void
Percolation::debug() const
{
    mUf->printConnectedComponants();
}
