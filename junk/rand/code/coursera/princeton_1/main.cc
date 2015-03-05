
#include "NaiveUnionFind.h"
#include "QuickUnionFind.h"
#include <cassert>
#include <iostream>

void
test(UnionFind& uf)
{
    std::cout << "test" << std::endl;

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

void
exercise1()
{
    std::cout << "exercise1" << std::endl;
    // 3-9 5-2 8-1 5-0 1-0 3-4 
    NaiveUnionFind nuf(10);

    nuf.Union(3, 9);
    nuf.Union(5, 2);
    nuf.Union(8, 1);
    nuf.Union(5, 0);
    nuf.Union(1, 0);
    nuf.Union(3, 4);

    nuf.print();
}

int
main()
{
    NaiveUnionFind nuf(10);
    test(nuf);

    QuickUnionFind quf(10);
    test(quf);

    QuickUnionFind wuf(10);
    test(wuf);

    exercise1();

    return 0;
}
