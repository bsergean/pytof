#include <vector>
#include <iostream>
#include <algorithm>

typedef std::vector<std::string> StringVec;
typedef std::pair<std::string, std::string> StringPair;

StringVec
anagrams(const StringVec& strings) 
{
    std::vector<StringPair> pairs;

    for (int i = 0; i < strings.size(); ++i) {
        std::string sortedString(strings[i]);
        std::sort(sortedString.begin(), sortedString.end());

        pairs.push_back(StringPair(sortedString, strings[i]));
    }

    std::sort(pairs.begin(), pairs.end());

    StringVec output;
    for (int i = 0; i < pairs.size(); ++i) {
        output.push_back(pairs[i].second);
    }

    return output; 
}

int
main()
{
    StringVec strings;
    strings.push_back("foo");
    strings.push_back("bar");
    strings.push_back("oof");
    strings.push_back("rab");

    StringVec groups = anagrams(strings);

    for (int i = 0; i < groups.size(); ++i) {
        std::cout << groups[i] << " ";
    }
    std::cout << std::endl;
}
