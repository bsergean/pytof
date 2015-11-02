
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
    TreeNode(int x, TreeNode* _left, TreeNode* _right) : val(x), left(_left), right(_right) {}
};

typedef std::vector<std::string> StringList;

std::vector<std::string> 
binaryTreePaths(TreeNode* root) 
{
    std::vector<std::string> paths;
    if (root == NULL) return paths;

    if (root->left == NULL && root->right == NULL) {
        std::stringstream ss;
        ss << root->val;
        paths.push_back(ss.str());
        return paths;
    }

    StringList leftPaths  = binaryTreePaths(root->left);
    StringList rightPaths = binaryTreePaths(root->right);
    
    int N;

    N = leftPaths.size();
    for (int i = 0; i < N; ++i) {
        std::string path = leftPaths[i];
        std::stringstream ss;
        ss << root->val;
        ss << "->";
        ss << path;
        leftPaths[i] = ss.str();
    }

    N = rightPaths.size();
    for (int i = 0; i < N; ++i) {
        std::string path = rightPaths[i];
        std::stringstream ss;
        ss << root->val;
        ss << "->";
        ss << path;
        rightPaths[i] = ss.str();
    }

    N = leftPaths.size();
    for (int i = 0; i < N; ++i) {
        std::string path = leftPaths[i];
        paths.push_back(path);
    }

    N = rightPaths.size();
    for (int i = 0; i < N; ++i) {
        std::string path = rightPaths[i];
        paths.push_back(path);
    }

    return paths;
}

int
main()
{
    // Constructed binary tree is
    //             1
    //           /   \
    //         2      3
    //       /  \
    //     4     5
    //

    TreeNode* one   = new TreeNode(1, NULL, NULL);
    TreeNode* two   = new TreeNode(2, NULL, NULL);
    TreeNode* three = new TreeNode(3, NULL, NULL);
    TreeNode* four  = new TreeNode(4, NULL, NULL);
    TreeNode* five  = new TreeNode(5, NULL, NULL);

    one->left = two;
    one->right = three;
    two->left = four;
    two->right = five;

    std::vector<std::string> paths;

    paths = binaryTreePaths(one);

    int N = paths.size();
    for (int i = 0; i < N; ++i) {
        std::cout << paths[i] << std::endl;
    }

    return 0;
}
