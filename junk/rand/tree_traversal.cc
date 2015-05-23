#include <iostream>
#include <queue>

struct Node {
    Node* left;
    Node* right;
    char val;

    Node(char _val, Node* _left, Node* _right) :
    left(_left), right(_right), val(_val) {}
};

void
inOrder(Node* root)
{
    if (root == NULL) return;

    inOrder(root->left);
    std::cout << root->val << " ";
    inOrder(root->right);
}

void
preOrder(Node* root)
{
    if (root == NULL) return;

    std::cout << root->val << " ";
    inOrder(root->left);
    inOrder(root->right);
}

void
postOrder(Node* root)
{
    if (root == NULL) return;

    inOrder(root->left);
    inOrder(root->right);
    std::cout << root->val << " ";
}

void
bfsOrder(Node* root)
{
    std::queue<Node*> queue;
    queue.push(root);

    while (!queue.empty()) {
        Node* node = queue.front();
        queue.pop();

        std::cout << node->val << " ";

        if (node->left != NULL) {
            queue.push(node->left);
        }
        if (node->right != NULL) {
            queue.push(node->right);
        }
    }
}

int
main()
{
    //         d
    //     b      f
    //  a    c  e    g

    Node a('a', NULL, NULL);
    Node c('c', NULL, NULL);
    Node e('e', NULL, NULL);
    Node g('g', NULL, NULL);

    Node b('b', &a, &c);
    Node f('f', &e, &g);

    Node d('d', &b, &f);

    inOrder(&d);
    std::cout << std::endl;

    preOrder(&d);
    std::cout << std::endl;

    postOrder(&d);
    std::cout << std::endl;

    bfsOrder(&d);
    std::cout << std::endl;
}


