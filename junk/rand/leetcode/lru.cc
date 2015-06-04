#include <list>
#include <map>
#include <iostream>

typedef std::pair<int, int> IntPair;
typedef std::list<IntPair> PairList;
typedef PairList::iterator PairListIt;
typedef std::map<int, PairListIt> Map;
typedef Map::iterator MapIt;

class LRUCache {
public:
    LRUCache(int capacity) : 
        mCapacity(capacity), mSize(0) {}
    
    int get(int key) {

        MapIt jt = mMap.find(key);
        if (jt == mMap.end()) {
            return -1;
        }

        PairListIt it = jt->second;
        int val = it->second;

        // as it was accessed last, move this element
        // to the back of the list
        mList.splice(mList.end(), mList, it);

        return val;
    }
    
    void set(int key, int value) {
        MapIt jt = mMap.find(key);
        if (jt != mMap.end()) {
            PairListIt it = jt->second;
            it->second = value;
            mList.splice(mList.end(), mList, it);
            return;
        }

        mList.push_back(IntPair(key, value));
        mSize++;

        PairListIt it = mList.end();
        it--;
        mMap[key] = it;

        if (mSize > mCapacity) {
            IntPair pair = mList.front();
            MapIt mapIt = mMap.find(pair.first);
            if (mapIt != mMap.end()) {
                mMap.erase(mapIt);
            }
            mList.pop_front();
            mSize--;
        }
    }

private:
    std::list<IntPair> mList;
    std::map<int, PairListIt> mMap;
    int mCapacity;
    int mSize;
};

void
tc1()
{
    // 2,[set(2,1),set(2,2),get(2),set(1,1),set(4,1),get(2)]
    LRUCache cache(2);
    cache.set(2, 1);
    cache.set(2, 2);
    std::cout << cache.get(2) << std::endl;
    cache.set(1, 1);
    cache.set(4, 1);
    std::cout << cache.get(2) << std::endl;

    // should print 2, -1
}

void
tc2()
{
    LRUCache cache(2);
    cache.set(2, 1);
    cache.set(1, 1);
    cache.set(2, 3);
    cache.set(4, 1);
    std::cout << cache.get(1) << std::endl;
    std::cout << cache.get(2) << std::endl;

    // should print -1, 3
}

int
main()
{
    tc2();
    return 0;
}
