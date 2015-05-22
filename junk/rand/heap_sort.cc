#include <queue>
#include <vector>
#include <set>
#include <iostream>

void
printVec(const std::vector<int>& vec)
{
    int N = vec.size();
    for (int i = 0; i < N; ++i) {
        std::cout << vec[i] << " ";
    }

    std::cout << std::endl;
}

void
heapSort(std::vector<int>& vec)
{
    int N = vec.size();

    std::priority_queue<int> pq;

    for (int i = 0; i < N; ++i) {
        pq.push(vec[i]);
    }

#if 0
    vec.clear();
    vec.reserve(N);

    while (!pq.empty()) {
        int val = pq.top();
        pq.pop();
        vec.push_back(val);
    }

    std::reverse(vec.begin(), vec.end());
#else
    for (int i = 0; i < N; ++i) {
        int val = pq.top();
        pq.pop();

        int j = N - 1 - i;
        vec[j] = val;
    }
#endif
}

int
main()
{
    std::vector<int> vec;
    vec.push_back(3);
    vec.push_back(1);
    vec.push_back(9);
    vec.push_back(7);
    vec.push_back(2);

    printVec(vec);
    heapSort(vec);
    printVec(vec);

    return 0;
}

