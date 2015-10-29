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

class Codec {
public:

    typedef std::string Address;
    typedef std::map<Address, int> ValTable;

    typedef std::pair<Address, Address> Childs;
    typedef std::map<Address, Childs> ChildTable;

    Address
    toAddr(TreeNode* root)
    {
        if (root == NULL) return Address("NULL");
        std::stringstream ss;
        ss << root;
        return Address(ss.str());
    }

    void
    makeValTable(TreeNode* root, ValTable& valTable)
    {
        if (root == NULL) return;

        valTable[toAddr(root)] = root->val;
        makeValTable(root->left, valTable);
        makeValTable(root->right, valTable);
    }

    void
    makeChildTable(TreeNode* root, ChildTable& childTable)
    {
        if (root == NULL) return;

        childTable[toAddr(root)] = Childs(toAddr(root->left),
                                          toAddr(root->right));

        makeChildTable(root->left, childTable);
        makeChildTable(root->right, childTable);
    }

    void
    serializeValTable(std::stringstream& ss, ValTable& valTable)
    {
        ss << valTable.size() << " ";

        ValTable::const_iterator it, itEnd;
        it    = valTable.begin();
        itEnd = valTable.end();

        for (; it != itEnd; ++it) {
            ss << it->first << " " << it->second << std::endl;
        }
    }

    void
    serializeChildTable(std::stringstream& ss, ChildTable& childTable)
    {
        ss << childTable.size() << " ";

        ChildTable::const_iterator it, itEnd;
        it    = childTable.begin();
        itEnd = childTable.end();

        for (; it != itEnd; ++it) {
            ss << it->first << " " 
               << it->second.first  << " " 
               << it->second.second << std::endl;
        }
    }

    // Encodes a tree to a single string.
    std::string serialize(TreeNode* root) {
        ValTable valTable;
        ChildTable childTable;

        makeValTable(root, valTable);
        makeChildTable(root, childTable);

        std::stringstream ss;
        ss << toAddr(root) << std::endl;
        serializeValTable(ss, valTable);
        serializeChildTable(ss, childTable);
        
        return ss.str();
    }

    // Decodes your encoded data to tree.
    TreeNode* deserialize(std::string data) {

        std::stringstream ss;
        ss << data;

        Address rootAddr;
        ss >> rootAddr;

        int N;
        ss >> N;

        // val table
        std::map<Address, TreeNode*> nodes;
        for (int i = 0 ; i < N; ++i) {

            int val;
            Address addr;
            ss >> addr;
            ss >> val;

            TreeNode* node = new TreeNode(val, NULL, NULL);

            nodes[addr] = node;
        }

        TreeNode* root = nodes[rootAddr];

        ss >> N;

        // child table
        for (int i = 0 ; i < N; ++i) {

            Address nodeAddr;
            Address leftAddr;
            Address rightAddr;

            ss >> nodeAddr;
            ss >> leftAddr;
            ss >> rightAddr;

            TreeNode* node  = nodes[nodeAddr];
            TreeNode* left  = nodes[leftAddr];
            TreeNode* right = nodes[rightAddr];

            node->left = left;
            node->right = right;
        }
        
        return root;
    }
};

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

    Codec codec;
    std::string data = codec.serialize(one);
    std::cout << data << std::endl;

    TreeNode* node = codec.deserialize(data);

    std::cout << " ==== read again =====" << std::endl;

    Codec codec2;
    std::string data2 = codec2.serialize(node);
    std::cout << data2 << std::endl;

    return 0;
}
