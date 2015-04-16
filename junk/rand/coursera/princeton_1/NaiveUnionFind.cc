#include "NaiveUnionFind.h"

#include <iostream>

NaiveUnionFind::NaiveUnionFind(int n)
    : UnionFind()
{ 
    mVec.resize(n); 
    for (uint i = 0; i < mVec.size(); ++i) {
        mVec[i] = i;
    }
}

void
NaiveUnionFind::print()
{
    for (uint i = 0; i < mVec.size(); ++i) {
        std::cout << mVec[i] << " ";
    }
    std::cout << std::endl;
}

bool
NaiveUnionFind::find(int n, int p) const
{
    return mVec[n] == mVec[p];
}

void 
NaiveUnionFind::Union(int n, int p)
{
    uint src =  mVec[n];
    uint tget = mVec[p];

    for (uint i = 0; i < mVec.size(); ++i) {
        if (mVec[i] == src) {
            mVec[i] = tget;
        }
    }
}

int 
NaiveUnionFind::printConnectedComponants() const
{
    ConnectedComponants sets;

    for (uint i = 0; i < mVec.size(); ++i) {
        sets[mVec[i]].push_back(i);
    }

    printSets(sets);

    return sets.size();
}

