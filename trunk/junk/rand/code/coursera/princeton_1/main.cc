
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
exercise1(UnionFind& uf)
{
    std::cout << "exercise1" << std::endl;

    uf.Union(3, 9);
    assert(uf.printConnectedComponants() == 9);
    uf.Union(5, 2);
    assert(uf.printConnectedComponants() == 8);
    uf.Union(8, 1);
    assert(uf.printConnectedComponants() == 7);
    uf.Union(5, 0);
    assert(uf.printConnectedComponants() == 6);
    uf.Union(1, 0);
    assert(uf.printConnectedComponants() == 5);
    uf.Union(3, 4);
    assert(uf.printConnectedComponants() == 4);

    uf.print();

    std::cout << "exercise1-test" << std::endl;
    uf.printConnectedComponants();
}

void
exercise2(UnionFind& uf)
{
    std::cout << "exercise2" << std::endl;
    // 6-9 5-7 2-4 1-5 5-8 8-0 4-6 1-9 3-7 

    uf.Union(6, 9);
    uf.Union(5, 7);
    uf.Union(2, 4);
    uf.Union(1, 5);
    uf.Union(5, 8);
    uf.Union(8, 0);
    uf.Union(4, 6);
    uf.Union(1, 9);
    uf.Union(3, 7);

    uf.print();

    std::cout << "exercise2-test" << std::endl;
    uf.printConnectedComponants();
}

void
exercise3(WeightedQuickUnionFind& uf)
{
    uint input1[] = { 2, 7, 1, 7, 7, 1, 7, 0, 7, 3 };
    uf.reset(input1, 10);
    uf.printStats();
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

    // 3-9 5-2 8-1 5-0 1-0 3-4 
    NaiveUnionFind nuf2(10);
    exercise1(nuf2);
    QuickUnionFind quf2(10);
    exercise1(quf2);
    WeightedQuickUnionFind wuf2(10);
    exercise1(wuf2);

    //WeightedQuickUnionFind wuf2(10);
    //exercise2(wuf2);

    WeightedQuickUnionFind wuf3(10);
    exercise3(wuf3);

    return 0;
}
