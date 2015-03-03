#include <iostream>
#include <vector>
#include <cassert>

typedef unsigned int uint;

class UnionFind
{
public:
    UnionFind(int n);
    void print();
    bool find(int n, int p);
    void Union(int n, int p);

private:
    std::vector<uint> mVec;
};

UnionFind::UnionFind(int n)
{ 
    mVec.resize(n); 
    for (uint i = 0; i < mVec.size(); ++i) {
        mVec[i] = i;
    }
}

void
UnionFind::print()
{
    for (uint i = 0; i < mVec.size(); ++i) {
        std::cout << mVec[i] << " ";
    }
    std::cout << std::endl;
}

bool
UnionFind::find(int n, int p)
{
    return mVec[n] == mVec[p];
}

void 
UnionFind::Union(int n, int p)
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
main()
{
    UnionFind uf(10);
    uf.print();
    
    uf.Union(3, 4);
    uf.print();

    uf.Union(0, 5);
    uf.print();

    uf.Union(5, 6);
    uf.print();

    assert(uf.find(0, 6));
    assert(uf.find(3, 4));
    assert(!uf.find(0, 4));

    uf.print();
}
