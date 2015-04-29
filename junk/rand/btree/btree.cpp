// vim: set tabstop=4 shiftwidth=4 expandtab:
//
// Binary search tree, with a parent pointer which makes it easier (for me :) to implement deletion.
// Not templated, storing integers
//
// walk method can be used to make sure to output and array and see if it's sorted.
//

#include <stdio.h>
#include <assert.h>
#include <stdlib.h>

#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

class Node
{
public:
    Node(int val, Node* parent = NULL) 
        : mVal(val)
        , mLeft(NULL)
        , mRight(NULL) 
        , mParent(parent) {}

    ~Node()
    {
        if (mLeft)  delete mLeft;
        if (mRight) delete mRight;

        if (mParent) {
            if (mParent->mLeft == this) {
                mParent->mLeft = NULL;
            }
            if (mParent->mRight == this) {
                mParent->mRight = NULL;
            }
        }
    }

    void insert(int val);
    Node* search(int val);
    void remove(int val);
    void walk(vector<int> *out);
    int elemCnt();
    void dotPrint(const std::string& fileName);

private:
    void dotPrint(std::stringstream& ss);

    Node* mLeft;
    Node* mRight;
    Node* mParent;
    int mVal;
};

Node* 
Node::search(int val)
{
    if (val < mVal) {
        if (mLeft) {
            return mLeft->search(val);
        } else {
            return NULL;
        }
    }

    if (val > mVal) {
        if (mRight) {
            return mRight->search(val);
        } else {
            return NULL;
        }
    }

    return this;
}

void 
Node::insert(int val)
{
    if (val < mVal) {
        if (mLeft) {
            mLeft->insert(val);
        } else {
            mLeft = new Node(val, this);
        }
    }

    if (val > mVal) {
        if (mRight) {
            mRight->insert(val);
        } else {
            mRight = new Node(val, this);
        }
    }
}

void 
Node::remove(int val)
{
    Node* cur    = this;
    while (cur && cur->mVal != val) {
        mParent = cur;
        if (val > cur->mVal) {
            cur = cur->mRight;
        } else {
            cur = cur->mLeft;
        }
    }

    if (!cur || cur->mVal != val) return;

    // The node has zero children
    if (cur->mLeft == NULL && cur->mRight == NULL) {
        delete cur;
        return;
    }

    // The node has one children
    bool left = mParent && mParent->mLeft && mParent->mLeft == cur;

    if (cur->mRight == NULL) {
        if (mParent) {
            if (left) {
                mParent->mLeft = cur->mLeft;
            } else {
                mParent->mRight = cur->mLeft;
            }
        }

        cur->mLeft = NULL;
        delete cur;
        return;
    }

    if (cur->mLeft == NULL) {
        if (mParent) {
            if (left) {
                mParent->mLeft = cur->mRight;
            } else {
                mParent->mRight = cur->mRight;
            }
        }

        cur->mRight = NULL;
        delete cur;
        return;
    }

    /* The node has two children: let's delete 3

       6
     /   \
    3     8
   / \   /
  1   4 7
       \
        5

     Become

       6
     /   \
    1     8
     \   /
      4 7
       \
       5

   If we delete 6
       5
     /   \
    1     8
     \   /
      4 7

       Here we looked for the biggest node on the left branch
       */

    // Search the biggest node on the left side
    Node* bigLeft = cur->mLeft;
    while (bigLeft->mRight) {
        bigLeft = bigLeft->mRight;
    }

    cur->mVal = bigLeft->mVal;
    bigLeft->remove(cur->mVal);
}

void 
Node::walk(vector<int> *out)
{
    if (mLeft) mLeft->walk(out);
    out->push_back( mVal );
    if (mRight) mRight->walk(out);
}

int 
Node::elemCnt()
{
    int res = 1;
    if (mLeft)  res += mLeft->elemCnt();
    if (mRight) res += mRight->elemCnt();

    return res;
}

/*
   graph tree {
   5 -- 3;
   5 -- 7;
   3 -- 1;
   3 -- 4;
   7 -- 6;
   }
   */
void 
Node::dotPrint(std::stringstream& ss)
{
    if (mLeft) {
        ss << "\t" << mVal << " -- " << mLeft->mVal << ";\n";
        mLeft->dotPrint(ss);
    }
    if (mRight) {
        ss << "\t" << mVal << " -- " << mRight->mVal << ";\n";
        mRight->dotPrint(ss);
    }
}

void 
Node::dotPrint(const std::string& fileName)
{
    std::stringstream ss;
    ss << "graph tree {\n";
    dotPrint(ss);
    ss << "}\n";

    if (fileName.empty()) {
        std::cout << ss.str();
    } else {
        FILE* stream = fopen(fileName.c_str(), "w");
        fprintf(stream, "%s", ss.str().c_str());
        fclose(stream);

        std::string command;
    }
}

/* walk and print */
void 
wprint(Node* n) 
{
    vector<int> output;
    n->walk(&output);

    for (int i = 0; i < output.size(); i++) {
        cout << output[i] << " ";
    }
    cout << endl;
}

int 
main()
{
    /* Our tree
       5
       /   \
       3     7
       / \   /
       1   4 6
       */
    Node* n = new Node(5);
    n->insert(3);
    n->insert(1);
    n->insert(4);
    n->insert(7);
    n->insert(6);

    n->dotPrint("tree.dot");

    wprint(n);
    // zero child
    n->remove(1);
    wprint(n);

    // One child right
    n->remove(7);
    wprint(n);

    // One child left
    n->remove(4);
    wprint(n);

    delete n;

    // Two childs
    /* The node has two children
    */
    n = new Node(6);
    n->insert(3);
    n->insert(8);
    n->insert(7);
    n->insert(1);
    n->insert(4);
    n->insert(5);

    //        6
    //      /   \
    //     3     8
    //    / \   /
    //   1   4 7
    //        \
    //         5

    n->dotPrint("tree.dot");

    wprint(n);
    n->remove(3);
    n->dotPrint("tree2.dot");
    wprint(n);
    n->remove(6);

    n->dotPrint("tree3.dot");

    // return 0;
    wprint(n);
    // exit(1);

    vector<int> input;
    FILE* fo = fopen("input.txt", "r");
    int cnt, tmp;
    fscanf(fo, "%d", &cnt);
    for (int i = 0; i < cnt; i++) {
        fscanf(fo, "%d", &tmp);
        input.push_back(tmp);
    }

    n = new Node(input[0]);
    for (int i = 1; i < input.size(); i++) {
        n->insert(input[i]);
    }

    vector<int> output;
    // output.reserve(n->elemCnt());
    output.reserve(100000);
    n->walk(&output);

    // search | remove
    assert( n->search(4925087) ); 
    printf( "%d\n", n->elemCnt() ); 
    n->remove(729811); // not present in input
    printf( "%d\n", n->elemCnt() ); 

    n->remove(4925087);
    assert( n->elemCnt() == 99 ); 

    return 0;
}
