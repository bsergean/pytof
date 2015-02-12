#include <string>
#include <iostream>
#include <iterator>
#include <cassert>

namespace bstl {

template <typename T>
struct Node {
    T mVal;
    Node<T>* mNext;
};

template <typename T>
class list
{
public:
    list();
    ~list();

    void push_back(const T& t);
    void pop_back();
    void push_front(const T& t);
    void pop_front();
    T& front();
    T& back();

    void clear();
    void remove(const T& t);
    size_t size();
    void merge(list& L);

    void print();

    // iterator
    class iterator : public std::iterator<std::input_iterator_tag, T>
    {
    public:
        iterator(Node<T>* node) { mCurr = node; }
        iterator() { mCurr = NULL; }

        iterator& operator++() { mCurr = mCurr->mNext; return *this; }

        bool operator!=(const iterator& rhs) { return mCurr != rhs.mCurr; }
        T& operator*() { return mCurr->mVal; }

    private:
        Node<T>* mCurr;
    };

    iterator begin() { return iterator(mHead); }
    iterator end()   { return iterator(); }

private:
    Node<T>* mHead;
    Node<T>* mTail;
};

template <typename T>
list<T>::list()
{
    mHead = NULL;
    mTail = NULL;
}

template <typename T>
list<T>::~list()
{
    clear();
}

template <typename T>
void
list<T>::clear()
{
    Node<T>* curr = mHead;
    Node<T>* temp = NULL;

    while (curr != NULL) {
        temp = curr;
        curr = curr->mNext;
        delete temp;
    }

    mHead = mTail = NULL;
}

template <typename T>
void 
list<T>::push_back(const T& t)
{
    Node<T>* next = new Node<T>();
    next->mVal  = t;
    next->mNext = NULL;

    if (mTail != NULL) {
        mTail->mNext = next;
    }
    mTail = next;

    if (mHead == NULL) {
        mHead = mTail;
    }
}

template <typename T>
void 
list<T>::pop_back()
{
    assert(mTail != NULL);

    Node<T>* prev = NULL;
    Node<T>* curr = mHead;

    while (curr != mTail) {
        prev = curr;
        curr = curr->mNext;
    }

    delete mTail;
    prev->mNext = NULL;
    mTail = prev;
}

template <typename T>
void 
list<T>::push_front(const T& t)
{
    Node<T>* next = new Node<T>();
    next->mVal  = t;
    next->mNext = mHead;

    mHead = next;

    if (mTail == NULL) {
        mTail = NULL;
    }
}

template <typename T>
void 
list<T>::pop_front()
{
    assert(mHead != NULL);

    Node<T>* temp = mHead;
    mHead = mHead->mNext;
    delete temp;
}

template <typename T>
T&
list<T>::front()
{
    assert(mHead != NULL);
    return mHead->mVal;
}

template <typename T>
T&
list<T>::back()
{
    assert(mTail != NULL);
    return mTail->mVal;
}

template <typename T>
size_t 
list<T>::size()
{
    size_t result = 0;
    Node<T>* curr = mHead;

    while (curr != NULL) {
        curr = curr->mNext;
        result++;
    }

    return result;
}

template <typename T>
void
list<T>::print()
{
    Node<T>* curr = mHead;

    while (curr != NULL) {
        std::cout << curr->mVal << " ";
        curr = curr->mNext;
    }
    std::cout << std::endl;
}

template <typename T>
void
list<T>::remove(const T& t)
{
    Node<T>* prev = NULL;
    Node<T>* curr = mHead;
    Node<T>* temp = mHead;
    bool deleteCurr = false;

    while (curr != NULL) {
        temp = curr;

        if (curr->mVal == t) {
            if (prev) {
                prev->mNext = curr->mNext; // relink
            }
            deleteCurr = true;

            if (curr == mHead) {
                mHead = curr->mNext;
            }
        }

        if (curr->mVal != t) {
            prev = curr;
        }
        curr = curr->mNext;

        if (deleteCurr) {
            delete temp;
            deleteCurr = false;
        }
    }
}

template <typename T>
void
list<T>::merge(list& L)
{
    Node<T>* currA = mHead;
    Node<T>* currB = L.mHead;

    return;

    for (;;) {
        T& a = currA->mVal;
        T& b = currB->mVal;

        if (a < b) {
            currA = currA->mNext;
            continue;
        }

        // insert b node

    }
}

}

int main()
{
    typedef bstl::list<std::string> StringList;
    StringList names;

    names.push_back("Sandrine");
    names.push_back("Benjamin");
    names.push_back("Irene");
    names.push_back("Charlotte");

    names.push_front("Celine");
    names.push_front("Luc");

    {
        StringList::iterator it, itEnd;
        it    = names.begin();
        itEnd = names.end();

        for (; it != itEnd; ++it) {
            std::cout << *it << std::endl;
        }
    }

    std::cout << names.size() << std::endl;
    names.print();

    std::cout << "front = " << names.front() << std::endl;
    std::cout << "back = "  << names.back()  << std::endl;

    // remove end
    names.pop_back();
    names.print();
    names.push_back("Charlotte");
    names.print();

    // remove front
    names.pop_front();
    names.print();
    names.push_front("Luc");
    names.print();

    // delete in the middle
    names.remove("Benjamin");
    names.print();

    // delete last
    names.remove("Charlotte");
    names.print();

    // delete first
    names.remove("Luc");
    names.print();

    {
        StringList::iterator it, itEnd;
        it    = names.begin();
        itEnd = names.end();

        for (; it != itEnd; ++it) {
            std::cout << *it << std::endl;
        }
    }

    // delete all
    names.clear();
    names.print();

    // empty list
    {
        StringList emptyList;
        StringList::iterator it, itEnd;
        it    = emptyList.begin();
        itEnd = emptyList.end();

        for (; it != itEnd; ++it) {
            std::cout << *it << std::endl;
        }
    }

    // merge
    StringList namesA, namesB;
    namesA.push_back("Benjamin");
    namesA.push_back("Charlotte");
    namesA.push_back("Irene");
    namesA.push_back("Sandrine");

    namesB.push_front("Celine");
    namesB.push_front("Luc");

    namesA.merge(namesB);
    namesA.print();
}
