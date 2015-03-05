#include "NaiveUnionFind.h"

#include <iostream>
#include <map>
#include <vector>

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
NaiveUnionFind::find(int n, int p)
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

void 
NaiveUnionFind::printConnectedComponants()
{
    typedef std::map<uint, std::vector<uint> > ConnectedComponants;
    typedef std::map<uint, std::vector<uint> >::const_iterator 
        ConnectedComponantsIterator;

    ConnectedComponants sets;

    for (uint i = 0; i < mVec.size(); ++i) {
        sets[mVec[i]].push_back(i);
    }

    std::cout << "set size " << sets.size() << std::endl;

    ConnectedComponantsIterator it, itEnd;
    it    = sets.begin();
    itEnd = sets.end();

    for (; it != itEnd; ++it) {

        std::cout << it->first << ": ";

        std::vector<uint> component = it->second;
        uint N = component.size();

        for (uint i = 0; i < N; ++i) {
            std::cout << component[i] << " ";
        }
        std::cout << std::endl;
    }
}

