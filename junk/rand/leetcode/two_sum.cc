#include <vector>
#include <iostream>

std::vector<int> 
twoSumQuadratic(std::vector<int>& nums, int target) 
{
    std::vector<int> out;
    int N = nums.size();

    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            if ((nums[i] + nums[j]) == target) {
                out.push_back(i+1);
                out.push_back(j+1);
                return out;
            }
        }
    }

    return out;
}

std::vector<int> 
twoSum(std::vector<int>& nums, int target) 
{
    typedef std::pair<int, int> IntPair;
    std::vector<IntPair> pairs;

    for (int i = 0; i < nums.size(); ++i) {
        pairs.push_back(IntPair(nums[i], i));
    }
    std::sort(pairs.begin(), pairs.end());

    std::vector<int> out;
    int N = nums.size();

    std::vector<IntPair>::const_iterator it;

    for (int i = 0; i < N; ++i) {
        //
        // search for target - nums[i]
        //
        int x = target - pairs[i].first;

        // binary search
        int lo = i + 1;
        int hi = N - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int y = pairs[mid].first;

            //
            // case1: lo   x    mid        hi
            //
            if (y > x) {
                hi = mid - 1;
            //
            // case2: lo       mid    y    hi
            //
            } else if (y < x) {
                lo = mid + 1;

            } else { // found !

                int u = pairs[i].second + 1;
                int v = pairs[mid].second + 1;
                if (u < v) {
                    out.push_back(u);
                    out.push_back(v);
                } else {
                    out.push_back(v);
                    out.push_back(u);
                }
                return out;
            }
        }
    }

    return out;
}

int
main()
{
    std::vector<int> nums;
    nums.push_back(2);
    nums.push_back(7);
    nums.push_back(11); 
    nums.push_back(15);
    nums.push_back(16);
    nums.push_back(16);
    nums.push_back(16);
    nums.push_back(16);
    nums.push_back(16);
    nums.push_back(16);

    std::vector<int> out = twoSum(nums, 9);
    for (int i = 0; i < out.size(); ++i) {
        std::cout << out[i] << " ";
    }
    std::cout << std::endl;
}

