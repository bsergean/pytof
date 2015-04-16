#pragma once

#include "UnionFind.h"
#include <vector>
#include <sstream>

class WeightedQuickUnionFind: public UnionFind
{
public:
    WeightedQuickUnionFind(int n);
    void print();
    bool find(int n, int p) const;
    void Union(int n, int p);

    int printConnectedComponants() const;
    void printStats() const;
    void reset(uint* input, uint size);
    void init(const std::string& str);
    void toPng(const std::string& filename) const;

private:
    int root(int n) const;
    int distanceToRoot(int n) const;
    void printAsDot(std::stringstream& ss) const;

    //
    // mVec is a forest (a list of tree)
    // Each entry contains its parent
    //
    std::vector<uint> mVec;
    std::vector<uint> mWeights;
};
