class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        
        int j = 0;
        int N = nums.size();
        
        for (int i = 0; i < N; ++i) {
            
            if (nums[i] != 0) {
                nums[j] = nums[i];
                ++j;
            }
        }
        
        for (int i = 0; i < (N - j) ; ++i) {
            int k = N-1-i;
            nums[k] = 0;
        }
    }
};
