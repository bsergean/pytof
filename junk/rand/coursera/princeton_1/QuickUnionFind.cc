#include "QuickUnionFind.h"

#include <iostream>
#include <cassert>

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
QuickUnionFind::root(int n) const
{
    uint result = mVec[n];
    while (result != mVec[result]) {
        result = mVec[result];
    }

    return result;
}

bool
QuickUnionFind::find(int n, int p) const
{
    return root(n) == root(p);
}

void 
QuickUnionFind::Union(int n, int p)
{
    int r = root(p);
    mVec[r] = mVec[n];
}

int
QuickUnionFind::printConnectedComponants() const
{
    ConnectedComponants sets;

    for (uint i = 0; i < mVec.size(); ++i) {
        sets[root(mVec[i])].push_back(i);
    }

    printSets(sets);

    return sets.size();
}
