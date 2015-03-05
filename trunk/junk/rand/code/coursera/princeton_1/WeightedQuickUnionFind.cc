#include "WeightedQuickUnionFind.h"

#include <iostream>
#include <cassert>

WeightedQuickUnionFind::WeightedQuickUnionFind(int n)
    : UnionFind()
{ 
    mVec.resize(n); 
    mWeights.resize(n); 

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

int
WeightedQuickUnionFind::distanceToRoot(int n)
{
    uint i = 0;
    uint result = mVec[n];
    while (result != mVec[result]) {
        assert(false);
        result = mVec[result];
        i++;
    }

    return i;
}

bool
WeightedQuickUnionFind::find(int n, int p)
{
    return root(n) == root(p);
}

void 
WeightedQuickUnionFind::Union(int n, int p)
{
    if (root(n) == root(p)) {
        return;
    }

    if (mWeights[n] > mWeights[p]) {
        mVec[p] = root(n);
        mWeights[n] += mWeights[p];
    } else {
        mVec[n] = root(p);
        mWeights[p] += mWeights[n];
    }
}

void 
WeightedQuickUnionFind::printConnectedComponants()
{
    for (uint i = 0; i < mVec.size(); ++i) {
        std::cout << i 
                  << " root " << root(i) 
                  << " distance " << distanceToRoot(i) 
                  << std::endl;
    }
}
