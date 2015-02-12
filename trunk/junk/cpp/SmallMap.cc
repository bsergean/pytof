#include <vector>
#include <string>

#include <iostream>

template <typename Key, typename T>
class SmallMap
{
public:
    SmallMap() {}

    T& operator[](const Key& key);

public:
    typedef typename std::vector< std::pair<const Key, T> >::iterator iterator;

    iterator begin() { return mElements.begin(); }
    iterator end() { return mElements.end(); }

private:
    std::vector< std::pair<const Key, T> > mElements;
};

// 
// http://stackoverflow.com/questions/495021/why-can-templates-only-be-implemented-in-the-header-file
//
template <typename Key, typename T>
T& 
SmallMap<Key, T>::operator[](const Key& key)
{
    for (unsigned i = 0, N = mElements.size(); i < N; ++i) {
        if (mElements[i].first == key) {
            return mElements[i].second;
        }
    }

    mElements.push_back(std::make_pair(key, T()));
    return mElements.back().second;
}

int main()
{
    SmallMap<std::string, size_t> files;

    files["/bin/ps"] = 46784;
    files["/bin/mkdir"] = 14592;

    std::cout << files["/bin/ps"] << std::endl;
    std::cout << files["/bin/mkdir"] << std::endl;

    SmallMap<std::string, size_t>::iterator it, itEnd;
    it    = files.begin();
    itEnd = files.end();

    for (; it != itEnd; ++it) {
        std::cout << it->first << " " << it->second << std::endl;
    }
}
