#include <vector>
#include <sstream>
#include "WeightedQuickUnionFind.h"

#pragma once

class Percolation {
public:
    // create N-by-N grid, with all sites blocked
    Percolation(int N);

    // open site (row i, column j) if it is not open already
    void open(int i, int j); 

    // is site (row i, column j) open?
    bool isOpen(int i, int j);

    // is site (row i, column j) full?
    bool isFull(int i, int j);

    // does the system percolate?
    bool percolates();

    void printToStream(std::stringstream& ss) const;
    void print() const;
    void debug() const;

private:
    void printPos(std::string msg, int i, int j, int k) const;

    std::vector<bool> mVec;
    uint mSize;
    uint mTop;
    uint mBottom;

    WeightedQuickUnionFind* mUf;
};
