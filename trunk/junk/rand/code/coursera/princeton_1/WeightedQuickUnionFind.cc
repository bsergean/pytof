#include "WeightedQuickUnionFind.h"

#include <iostream>

WeightedQuickUnionFind::WeightedQuickUnionFind(int n)
    : UnionFind()
{ 
    mVec.resize(n); 
    for (uint i = 0; i < mVec.size(); ++i) {
        mVec[i] = i;
        mWeights[i] = 1;
    }
}

void
WeightedQuickUnionFind::print()
{
    for (uint i = 0; i < mVec.size(); ++i) {
        std::cout << mVec[i] << " ";
    }
    std::cout << std::endl;
}

int
WeightedQuickUnionFind::root(int n)
{
    uint result = mVec[n];
    while (result != mVec[result]) {
        result = mVec[result];
    }

    return result;
}

bool
WeightedQuickUnionFind::find(int n, int p)
{
    return root(n) == root(p);
}

void 
WeightedQuickUnionFind::Union(int n, int p)
{
    if (mWeights[n] > mWeights[p]) {
        mVec[p] = root(n);
        mWeights[n] += mWeights[p];
    } else {
        mVec[n] = root(p);
        mWeights[p] += mWeights[n];
    }
}

