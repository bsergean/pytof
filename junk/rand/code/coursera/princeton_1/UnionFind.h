#pragma once

typedef unsigned int uint;

class UnionFind
{
public:
    virtual void print() = 0;
    virtual bool find(int n, int p) = 0;
    virtual void Union(int n, int p) = 0;
};
