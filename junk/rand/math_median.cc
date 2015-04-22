#include <vector>
#include <iostream>
#include <algorithm>

void
computeMedian(std::vector<int>& vec)
{
    std::sort(vec.begin(), vec.end());

    if ((vec.size() % 2) == 0) {
        int mid = vec.size() / 2;
        float median = (vec[mid] + vec[mid+1]) / 2.0f;
        std::cout << median << std::endl;
    } else {
        std::cout << vec[vec.size() / 2] << std::endl;
    }
}

int main()
{
    std::vector<int> vec;
    vec.push_back(1);
    vec.push_back(2);
    vec.push_back(3);

    computeMedian(vec);

    vec.clear();
    vec.push_back(1);
    vec.push_back(2);
    vec.push_back(3);
    vec.push_back(4);

    computeMedian(vec);

    return 0;
}
