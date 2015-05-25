#include <map>
#include <vector>
#include <string>
#include <set>
#include <iostream>
#include <cassert>

// does not work with sorting
std::vector<int>
signature(const std::string& str)
{
    typedef std::map<char, int> OccurenceMap;
    typedef std::map<char, int>::iterator OccurenceMapIt;
    
    OccurenceMap occurences;
    OccurenceMapIt it;
    
    for (int i = 0; i < str.size(); ++i) {
        char c = str[i];
        it = occurences.find(c);
        if (it == occurences.end()) { // no hit
            occurences[c] = 1;
        } else { // hit
            occurences[c] += 1;
        }
    }
    
    std::vector<int> out;
    
    for (it = occurences.begin(); it != occurences.end(); ++it) {
        out.push_back(it->second);
    }
    
    std::sort(out.begin(), out.end());
    
    return out;
}

bool 
isIsomorphicBad(std::string s, std::string t) 
{
    std::vector<int> sig1 = signature(s);
    std::vector<int> sig2 = signature(t);

    std::cout << "Sig 1: ";
    for (int i = 0; i < sig1.size(); ++i) {
        std::cout << sig1[i] << " ";
    }
    std::cout << std::endl;

    std::cout << "Sig 2: ";
    for (int i = 0; i < sig2.size(); ++i) {
        std::cout << sig2[i] << " ";
    }
    std::cout << std::endl;

    return sig1 == sig2;
}

bool 
isIsomorphic(std::string s, std::string t) 
{
    std::cout << "isIsomorphic: " << s << ", " << t << std::endl;

    typedef std::map<char, char> ConversionTable;
    typedef std::map<char, char>::iterator ConversionTableIterator;
    ConversionTable conversionTable;
    ConversionTableIterator it;

    std::set<char> converted;

    for (int i = 0; i < t.size(); ++i) {
        char from = s[i];
        char to = t[i];

        std::cout << "from = " << from << " to = " << to << std::endl;
        
        char expectedConversion;

        it = conversionTable.find(from);
        if (it == conversionTable.end()) {

            std::cout << "from not in table" << std::endl;
            conversionTable[from] = to;

            if (converted.count(to) != 0) {
                return false;
            }

            converted.insert(to);
            continue;
        } else {
            std::cout << "from is in table" << std::endl;
            expectedConversion = it->second;

            std::cout << "from " << from << " maps to " << expectedConversion << std::endl;
            std::cout << "to is " << to << std::endl;

            if (expectedConversion != to) {
                return false;
            }
        }
    }

    return true;
}

int
main()
{
    assert(isIsomorphic("aba", "baa") == false);
    assert(isIsomorphic("foo", "bar") == false);
    assert(isIsomorphic("ab", "aa") == false);

    assert(isIsomorphic("egg", "add"));
    assert(isIsomorphic("paper", "title"));

    return 0;
}
