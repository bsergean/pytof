#include "UnionFind.h"
#include <vector>

class QuickUnionFind: public UnionFind
{
public:
    QuickUnionFind(int n);
    void print();
    bool find(int n, int p) const;
    void Union(int n, int p);

    int printConnectedComponants() const;

private:
    int root(int n) const;
    int distanceToRoot(int n) const;

    //
    // mVec is a forest (a list of tree)
    // Each entry contains its parent
    //
    std::vector<uint> mVec;
};

