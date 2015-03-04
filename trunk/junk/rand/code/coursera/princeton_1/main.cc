
#include "NaiveUnionFind.h"
#include <cassert>

void
test(UnionFind& uf)
{
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

int
main()
{
    NaiveUnionFind uf(10);
    test(uf);

    return 0;
}
