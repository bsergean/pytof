
#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <map>
#include <sstream>

// Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x, TreeNode* _left = NULL, TreeNode* _right = NULL) : val(x), left(_left), right(_right) {}
};

typedef std::vector<int> IntVec;

void
printVec(const IntVec& nums)
{
    int N = nums.size();
    for (int i = 0; i < N; ++i) {
        std::cout << nums[i] << " ";
    }
    std::cout << std::endl;
}

TreeNode*
sortedArrayToBSTUtil(const IntVec& nums, int lo, int hi)
{
    int mid = (lo + hi) / 2;

    if (lo >= hi) {
        return NULL;
    }

    int val = nums[mid];
    TreeNode* root = new TreeNode(val);

    root->left  = sortedArrayToBSTUtil(nums, lo, mid);
    root->right = sortedArrayToBSTUtil(nums, mid + 1, hi);

    return root;
}

TreeNode* 
sortedArrayToBST(std::vector<int>& nums) 
{
    return sortedArrayToBSTUtil(nums, 0, nums.size());
}

void
printBST(TreeNode* root)
{
    if (root == NULL) return;
    printBST(root->left);
    std::cout << root->val << " ";
    printBST(root->right);
}

int
main()
{
    TreeNode* root = NULL;
    IntVec nums;

    for (int i = 0; i < 11; ++i) {
        nums.push_back(i);
    }

    root = sortedArrayToBST(nums);
    printBST(root);
    std::cout << std::endl;

    return 0;
}
