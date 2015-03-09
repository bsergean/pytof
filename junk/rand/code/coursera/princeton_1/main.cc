
#include "NaiveUnionFind.h"
#include "QuickUnionFind.h"
#include "WeightedQuickUnionFind.h"
#include "Percolation.h"
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

#if 0
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
#else
    // 7-0 2-7 1-3 9-6 6-7 8-6 
    uf.Union(7, 0);
    uf.Union(2, 7);
    uf.Union(1, 3);
    uf.Union(9, 6);
    uf.Union(6, 7);
    uf.Union(8, 6);
#endif

    uf.print();

    std::cout << "exercise1-test" << std::endl;
    uf.printConnectedComponants();
}

void
exercise2(UnionFind& uf)
{
    std::cout << "exercise2" << std::endl;
    // 6-9 5-7 2-4 1-5 5-8 8-0 4-6 1-9 3-7 

#if 0
    uf.Union(6, 9);
    uf.Union(5, 7);
    uf.Union(2, 4);
    uf.Union(1, 5);
    uf.Union(5, 8);
    uf.Union(8, 0);
    uf.Union(4, 6);
    uf.Union(1, 9);
    uf.Union(3, 7);
#else
    // 8-6 6-3 7-2 5-0 8-1 0-7 8-4 4-5 2-9 
    uf.Union(8, 6);
    uf.Union(6, 3);
    uf.Union(7, 2);
    uf.Union(5, 0);
    uf.Union(8, 1);
    uf.Union(0, 7);
    uf.Union(8, 4);
    uf.Union(4, 5);
    uf.Union(2, 9);
#endif

    uf.print();

    //std::cout << "exercise2-test" << std::endl;
    //uf.printConnectedComponants();
}

void
exercise3(WeightedQuickUnionFind& uf)
{
    /*
    2 7 1 7 7 1 7 0 7 3 
    2 5 2 4 2 4 4 2 2 2 
    0 2 7 9 1 1 6 6 2 6 
    6 7 2 6 6 4 2 6 2 2 
    0 0 2 3 5 5 6 7 9 9 
     */
    uint input1[] = { 2, 7, 1, 7, 7, 1, 7, 0, 7, 3 };
    uf.reset(input1, 10);
    uf.toPng("out1.png");

    uint input2[] = { 2, 5, 2, 4, 2, 4, 4, 2, 2, 2 };
    uf.reset(input2, 10);
    uf.toPng("out2.png");

    uint input3[] = { 0, 2, 7, 9, 1, 1, 6, 6, 2, 6 };
    uf.reset(input3, 10);
    uf.toPng("out3.png");

    uint input4[] = { 6, 7, 2, 6, 6, 4, 2, 6, 2, 2 };
    uf.reset(input4, 10);
    uf.toPng("out4.png");

    uint input5[] = { 0, 0, 2, 3, 5, 5, 6, 7, 9, 9 };
    uf.reset(input5, 10);
    uf.toPng("out5.png");
}

void
exercise3Bis(WeightedQuickUnionFind& uf)
{
    // cycle
    uf.init("6 7 6 7 6 6 8 6 3 0 ");
    uf.toPng("out1.png");

    // BAD
    // size of tree rooted as 8 than twice the size
    // of the parent of 8
    uf.init("7 7 8 8 6 8 6 8 6 8");
    uf.toPng("out2.png");

    // ok
    uf.init("7 7 7 2 5 0 7 7 7 0");
    uf.toPng("out3.png");

    // too tall
    uf.init("0 5 7 0 3 0 9 7 6 3 ");
    uf.toPng("out4.png");

    // ok (flat)
    uf.init("7 7 2 3 4 5 6 7 8 1 ");
    uf.toPng("out5.png");
}

void
exercise()
{
    NaiveUnionFind nuf(10);
    //test(nuf);

    QuickUnionFind quf(10);
    //test(quf);

    WeightedQuickUnionFind wuf(10);
    //test(wuf);

    // 3-9 5-2 8-1 5-0 1-0 3-4 
    NaiveUnionFind nuf2(10);
    exercise1(nuf2);

    QuickUnionFind quf2(10);
    //exercise1(quf2);
    WeightedQuickUnionFind wuf2(10);
    //exercise1(wuf2);

    WeightedQuickUnionFind wuf3(10);
    exercise2(wuf3);

    WeightedQuickUnionFind wuf4(10);
    //exercise3(wuf4);

    //exercise3Bis(wuf4);
}

void
testAssignment1()
{
    Percolation percolation(5);
    // percolation.print();

    percolation.open(0, 0);
    percolation.open(1, 0);
    percolation.open(2, 0);
    percolation.open(3, 0);
    percolation.open(4, 0);

    // percolation.debug();

    std::cout << std::endl;
    // percolation.print();

    assert(percolation.percolates());
}

void
testAssignment2()
{
    Percolation percolation(5);
    percolation.print();

    percolation.open(0, 4);
    percolation.open(1, 4);
    percolation.open(1, 3);
    percolation.open(2, 3);
    percolation.open(3, 3);
    percolation.open(3, 4);
    percolation.open(4, 4);

    // percolation.debug();

    std::cout << std::endl;
    percolation.print();

    std::cout << "Percolates: " 
              << percolation.percolates() << std::endl;
}

void
assignment()
{
    testAssignment1();
    testAssignment2();
}

int
main()
{
    assignment();

    return 0;
}
