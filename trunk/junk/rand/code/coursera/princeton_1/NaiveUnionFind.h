#include "UnionFind.h"
#include <vector>

class NaiveUnionFind: public UnionFind
{
public:
    NaiveUnionFind(int n);
    void print();
    bool find(int n, int p);
    void Union(int n, int p);
    void printConnectedComponants();

private:
    std::vector<uint> mVec;
};

