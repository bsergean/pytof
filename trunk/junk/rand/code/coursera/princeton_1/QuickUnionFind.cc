#include "QuickUnionFind.h"

#include <iostream>

QuickUnionFind::QuickUnionFind(int n)
    : UnionFind()
{ 
    mVec.resize(n); 
    for (uint i = 0; i < mVec.size(); ++i) {
        mVec[i] = i;
    }
}

void
QuickUnionFind::print()
{
    for (uint i = 0; i < mVec.size(); ++i) {
        std::cout << mVec[i] << " ";
    }
    std::cout << std::endl;
}

int
QuickUnionFind::root(int n)
{
    uint result = mVec[n];
    while (result != mVec[result]) {
        result = mVec[result];
    }

    return result;
}

bool
QuickUnionFind::find(int n, int p)
{
    return root(n) == root(p);
}

void 
QuickUnionFind::Union(int n, int p)
{
    mVec[n] = root(p);
}

