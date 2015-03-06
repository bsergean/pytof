#pragma once

#include <map>
#include <vector>

typedef unsigned int uint;

typedef std::map<uint, std::vector<uint> > ConnectedComponants;
typedef std::map<uint, std::vector<uint> >::const_iterator 
    ConnectedComponantsIterator;

class UnionFind
{
public:
    virtual void print() = 0;
    virtual bool find(int n, int p) const = 0 ;
    virtual void Union(int n, int p) = 0;
    virtual int printConnectedComponants() const = 0;

protected:
    void printSets(ConnectedComponants sets) const;
};
