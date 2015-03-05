
#include "NaiveUnionFind.h"
#include "QuickUnionFind.h"
#include "WeightedQuickUnionFind.h"
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

    std::cout << "exercise1-test" << std::endl;
    nuf.printConnectedComponants();
}

void
exercise2()
{
    std::cout << "exercise2" << std::endl;
    // 6-9 5-7 2-4 1-5 5-8 8-0 4-6 1-9 3-7 
    WeightedQuickUnionFind wuf(10);

    wuf.Union(6, 9);
    wuf.Union(5, 7);
    wuf.Union(2, 4);
    wuf.Union(1, 5);
    wuf.Union(5, 8);
    wuf.Union(8, 0);
    wuf.Union(4, 6);
    wuf.Union(1, 9);
    wuf.Union(3, 7);

    wuf.print();

    std::cout << "exercise2-test" << std::endl;
    wuf.printConnectedComponants();
}

int
main()
{
    NaiveUnionFind nuf(10);
    test(nuf);

    QuickUnionFind quf(10);
    test(quf);

    WeightedQuickUnionFind wuf(10);
    test(wuf);

    exercise1();
    exercise2();

    return 0;
}
