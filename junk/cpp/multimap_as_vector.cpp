
#include <assert.h>
#include <vector>
using namespace std;

typedef unsigned int uint;

class Bucket
{
public:
    Bucket();
    ~Bucket();
    void push(uint value);
    uint at(uint idx) const;
    uint size() const;

private:
    uint mV0;
    uint mV1;
    uint mV2;
    uint mV3;
    uint mCount;
    std::vector<uint>* mOthers;
} __attribute__ ((aligned)); // ~25% faster when creating lots of those

#define MAX_UINT 1 << 31 // must be something like that
#define ELEMS 4

Bucket::Bucket() : 
  mV0(MAX_UINT)
, mV1(MAX_UINT)
, mV2(MAX_UINT)
, mV3(MAX_UINT)
, mCount(0)
, mOthers(NULL)
{}

Bucket::~Bucket()
{
    delete mOthers;
}

void
Bucket::push(uint value)
{
    switch (mCount) {
    case 0: mV0 = value; break;
    case 1: mV1 = value; break;
    case 2: mV2 = value; break;
    case 3: mV3 = value; break;
    default:
        if (mOthers == NULL) {
            mOthers = new std::vector<uint>;
        }
        mOthers->push_back(value);
    }
    mCount++;
}

uint
Bucket::at(uint i) const
{
    assert(i < mCount);

    switch (i) {
    case 0:  return mV0;
    case 1:  return mV1;
    case 2:  return mV2;
    case 3:  return mV3;
    default: return (*mOthers)[i-ELEMS];
    }
}

uint
Bucket::size() const
{
    return mCount;
}

class MultiMap
{
public:
    MultiMap(uint size);
    void insert(uint key, uint value);
    const Bucket& at(uint i);

private:
    std::vector<Bucket> mBuckets;
};

MultiMap::MultiMap(uint size)
{
    mBuckets.resize(size);
}

void
MultiMap::insert(uint key, uint value)
{
    assert(key < mBuckets.size());

    Bucket& bucket = mBuckets[key];
    bucket.push(value);
}

const Bucket&
MultiMap::at(uint i)
{
    assert(i < mBuckets.size());

    return mBuckets[i];
}

int main()
{
    MultiMap mm(10);

    mm.insert(0, 1);
    mm.insert(0, 2);
    mm.insert(0, 3);
    mm.insert(0, 4);
    mm.insert(0, 5);
    mm.insert(0, 7);

    const Bucket& bucket = mm.at(0);
    for (uint i = 0; i < bucket.size(); ++i) {
        uint elem = bucket.at(i);
    }

    for (uint i = 0; i < 50000; ++i) {
        MultiMap mm(2000);
    }
}
