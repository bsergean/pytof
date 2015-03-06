
#include "UnionFind.h"
#include <iostream>

void 
UnionFind::printSets(ConnectedComponants sets) const
{
    std::cout << "set size " << sets.size() << std::endl;

    ConnectedComponantsIterator it, itEnd;
    it    = sets.begin();
    itEnd = sets.end();

    for (; it != itEnd; ++it) {

        std::cout << it->first << ": ";

        std::vector<uint> component = it->second;
        uint N = component.size();

        for (uint i = 0; i < N; ++i) {
            std::cout << component[i] << " ";
        }
        std::cout << std::endl;
    }
}
