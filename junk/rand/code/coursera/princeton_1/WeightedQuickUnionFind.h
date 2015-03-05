#include "UnionFind.h"
#include <vector>

class WeightedQuickUnionFind: public UnionFind
{
public:
    WeightedQuickUnionFind(int n);
    void print();
    bool find(int n, int p);
    void Union(int n, int p);

private:
    int root(int n);

    //
    // mVec is a forest (a list of tree)
    // Each entry contains its parent
    //
    std::vector<uint> mVec;
    std::vector<uint> mWeights;
};
