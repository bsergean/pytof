#include <iostream>

// Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x, TreeNode* _left, TreeNode* _right) : val(x), left(_left), right(_right) {}
};

void
minDepthHelper(TreeNode* root, int depth, int& min) 
{
    if (root->left == NULL && root->right == NULL) { 
        if (depth <= min) min = depth;
        return;
    }

    if (root->left != NULL) minDepthHelper(root->left, depth+1, min); 
    if (root->right != NULL) minDepthHelper(root->right, depth+1, min); 
}

int 
minDepth(TreeNode* root) 
{
    if (root == NULL) return 0;

    PriorityQueue pq;
    int min = 1000000000;
    minDepthHelper(root, 1, min);
    return min;
}

int
main()
{
    /*
           d
         b  
       a   c
     e       

     */
    
    TreeNode* F = new TreeNode(1, NULL, NULL);
    TreeNode* E = new TreeNode(1, NULL, NULL);
    TreeNode* C = new TreeNode(1, NULL, NULL);

    TreeNode* A = new TreeNode(1, E, NULL);
    TreeNode* B = new TreeNode(1, A, C);
    TreeNode* D = new TreeNode(1, B, NULL);

    std::cout << minDepth(D) << std::endl;

    return 0;
}
