#include "UnionFind.h"
#include <vector>

class NaiveUnionFind: public UnionFind
{
public:
    NaiveUnionFind(int n);
    void print();
    bool find(int n, int p) const;
    void Union(int n, int p);
    int printConnectedComponants() const;

private:
    std::vector<uint> mVec;
};

