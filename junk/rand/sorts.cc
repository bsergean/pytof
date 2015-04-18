#include <vector>
#include <iostream>
#include <cassert>

void
print(const std::vector<int>& vec)
{
    for (int i = 0; i < vec.size(); ++i) {
        std::cout << vec[i] << " ";
    }
    std::cout << std::endl;
}

void
printSubVec(const std::vector<int>& vec, int lo, int hi)
{
    for (int i = lo; i <= hi; ++i) {
        std::cout << vec[i] << " ";
    }
    std::cout << std::endl;
}

// selection sort
void
sort(std::vector<int>& vec)
{
    int N = vec.size();
    for (int i = 0; i < N; ++i) {
        for (int j = i; j < N; ++j) {

            if (vec[j] < vec[i]) {
                int tmp = vec[j];
                vec[j] = vec[i];
                vec[i] = tmp;
            }
        }
    }
}

int
partition(std::vector<int>& vec, int pivot, int lo, int hi)
{
    std::cout << "pivot " << pivot << " " << " lo " << lo << " hi " << hi << std::endl;

    std::vector<int> tmp;
    for (int i = lo; i <= hi; ++i) {
        if (vec[i] < pivot) {
            tmp.push_back(vec[i]);
        }
    }

    for (int i = lo; i <= hi; ++i) {
        if (vec[i] == pivot) {
            tmp.push_back(vec[i]);
        }
    }

    for (int i = lo; i <= hi; ++i) {
        if (vec[i] > pivot) {
            tmp.push_back(vec[i]);
        }
    }

    // copy back
    int j = 0;
    for (int i = lo; i <= hi; ++i) {
        vec[i] = tmp[j++];
    }

    printSubVec(vec, lo, hi);

    // where is my pivot at ?
    for (int i = lo; i <= hi; ++i) {
        if (vec[i] == pivot) {
            return i;
        }
    }

    assert(false);
    return -1;
}

void
sortRec(std::vector<int>& vec, int lo, int hi)
{
    if (lo > hi) return;

    int pivot = vec[lo];
    int mid = partition(vec, pivot, lo, hi);
    
    sortRec(vec, lo, mid-1);
    sortRec(vec, mid+1, hi);
}

void
sort2(std::vector<int>& vec)
{
    sortRec(vec, 0, vec.size() - 1);
}

#if 0
i j  prev vec
0 0       3 4 2 1 -1
1 1  0    3 4 2 1 -1  .... 
#endif

// insertion sort
void
sort3(std::vector<int>& vec)
{
    int N = vec.size();
    for (int i = 0; i < N; ++i) {

        for (int j = i; j > 0; --j) {

            int prev = j-1; // FIXME bound pb ?

            if (vec[prev] > vec[j]) { // need to re-order
                int tmp = vec[j];
                vec[j] = vec[prev];
                vec[prev] = tmp;
            }
        }
    }
}

int
main()
{
    std::vector<int> vec;
    vec.push_back(4);
    vec.push_back(3);
    vec.push_back(2);
    vec.push_back(1);
    vec.push_back(-1);
    print(vec);
    //sort(vec);
    //sort2(vec);
    sort3(vec);
    print(vec);
}
