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
WeightedQuickUnionFind::root(int n) const
{
    uint result = mVec[n];
    while (result != mVec[result]) {
        result = mVec[result];
    }

    return result;
}

int
WeightedQuickUnionFind::distanceToRoot(int n) const
{
    uint i = 0;
    uint result = mVec[n];
    while (result != mVec[result]) {
        result = mVec[result];
        i++;
    }

    return i;
}

bool
WeightedQuickUnionFind::find(int n, int p) const
{
    return root(n) == root(p);
}

void 
WeightedQuickUnionFind::Union(int n, int p)
{
    if (root(n) == root(p)) {
        return;
    }

    int rootN = root(n);
    int rootP = root(p);

    if (mWeights[rootN] < mWeights[rootP]) {
        int r = root(n);
        mVec[rootP] = r;
        mWeights[n] += mWeights[p];
    } else {
        int r = root(p);
        mVec[rootN] = r;
        mWeights[p] += mWeights[n];
    }
}

void 
WeightedQuickUnionFind::printStats() const
{
    std::cout << "caca" << std::endl;
    for (uint i = 0; i < mVec.size(); ++i) {
        std::cout << "pipi" << std::endl;
        std::cout << i 
                  << " root " << root(i) 
                  << " distance " << distanceToRoot(i) 
                  << std::endl;
    }
}

int
WeightedQuickUnionFind::printConnectedComponants() const
{
    ConnectedComponants sets;

    for (uint i = 0; i < mVec.size(); ++i) {
        sets[root(mVec[i])].push_back(i);
    }

    printSets(sets);

    return sets.size();
}

void 
WeightedQuickUnionFind::reset(uint* input, uint size)
{
    mVec.clear();
    for (uint i = 0; i < size; ++i) {
        mVec.push_back(input[i]);
    }
}

//
// http://eli.thegreenplace.net/2009/11/23/visualizing-binary-trees-with-graphviz
//
void 
WeightedQuickUnionFind::printAsDot() const
{
    std::cout << "digraph UF {" << std::endl;
    std::cout << "}" << std::endl;
}
