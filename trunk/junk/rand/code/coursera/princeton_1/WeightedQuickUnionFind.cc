#include "WeightedQuickUnionFind.h"

#include <iostream>
#include <cassert>
#include <unistd.h>

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
    int rootN = root(n);
    int rootP = root(p);

    if (rootN == rootP) {
        return;
    }

    if (mWeights[rootN] < mWeights[rootP]) {
        mVec[rootN] = rootP;
        mWeights[p] += mWeights[n];
    } else {
        mVec[rootP] = rootN;
        mWeights[n] += mWeights[p];
    }

    print();
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

void 
WeightedQuickUnionFind::init(const std::string& str)
{
    mVec.clear();

    std::stringstream ss;
    ss << str;

    while (! ss.eof()) {
        uint i;
        ss >> i;
        mVec.push_back(i);
    }
}

//
// http://eli.thegreenplace.net/2009/11/23/visualizing-binary-trees-with-graphviz
//
void 
WeightedQuickUnionFind::printAsDot(std::stringstream& ss) const
{
    ss << "digraph UF {" << std::endl;
    for (uint i = 0, N = mVec.size(); i < N; ++i) {
        ss << "\t" << i << " -> " << mVec[i] << std::endl;
    }
    ss << "}" << std::endl;
}

void 
WeightedQuickUnionFind::toPng(const std::string& filename) const
{
    std::string dotFilename(filename);
    dotFilename += ".dot";
    unlink(dotFilename.c_str());

    std::stringstream ss;
    printAsDot(ss);
    FILE* stream = fopen(dotFilename.c_str(), "w");
    fprintf(stream, "%s", ss.str().c_str());
    fclose(stream);

    char cmd[128];
    sprintf(cmd, "dot -Tpng %s > %s", 
            dotFilename.c_str(), filename.c_str());
    int ret = system(cmd);
    assert(ret == 0);

    // cleanup
    unlink(dotFilename.c_str());
}
