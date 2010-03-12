// vim: set tabstop=4 shiftwidth=4 expandtab:

#include <stdio.h>
#include <assert.h>
#include <stdlib.h>

#include <iostream>
#include <vector>
using namespace std;

#include "chrono.h"

class Node
{
public:
	Node(int val, Node* parent = 0): mVal(val), mLeft(0), mRight(0) {}
	~Node()
	{
		if (mLeft) delete mLeft;
		if (mRight) delete mRight;
	}

	void insert(int val);
	Node* search(int val);
	void remove(int val);
	void walk(vector<int> *out);
	int elemCnt();

private:
    void nullify_node(Node* cur, Node* parent);

	Node* mLeft;
	Node* mRight;
	int mVal;
};

Node* Node::search(int val)
{
	if (val < mVal)
		if (mLeft)
			return mLeft->search(val);
        else
            return 0;

	if (val > mVal)
		if (mRight)
			return mRight->search(val);
        else
            return 0;

    return this;
}

void Node::nullify_node(Node* cur, Node* parent)
{
    if (parent->mRight == cur)
        parent->mRight = 0;
    else
        parent->mLeft = 0;
}

void Node::remove(int val)
{
    Node* cur = this;
    Node* parent;
    while (cur && cur->mVal != val) {
        parent = cur;
        if (val > cur->mVal)
            cur = cur->mRight;
        else
            cur = cur->mLeft;
    }

    if (!cur || cur->mVal != val) return;

    // The node has zero children
    if (cur->mLeft == 0 && cur->mRight == 0) {
        nullify_node(cur, parent);
        delete cur;
        return;
    }

    // The node has one children
    bool left = parent->mLeft && parent->mLeft == cur;

    if (cur->mRight == 0) {
        if (parent)
            if (left)
                parent->mLeft = cur->mLeft;
            else
                parent->mRight = cur->mLeft;

        cur->mLeft = 0;
        delete cur;
        return;
    }
    if (cur->mLeft == 0) {
        if (parent)
            if (left)
                parent->mLeft = cur->mRight;
            else
                parent->mRight = cur->mRight;

        cur->mRight = 0;
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
    while (bigLeft->mRight)
        bigLeft = bigLeft->mRight;

    // bigLeft right node is NULL, set it to the right subtree
    bigLeft->mRight = cur->mRight;
    if (parent)
        parent->mLeft = bigLeft; 
    
    if (bigLeft != cur->mLeft)
        bigLeft->mLeft = cur->mLeft;

    // delete cur
    cur->mRight = cur->mLeft = 0;
    delete cur;
    
    // printf("%d\n", bigLeft->mVal);
}

void Node::insert(int val)
{
	if (val < mVal)
		if (mLeft)
			mLeft->insert(val);
		else
			mLeft = new Node(val, this);

	if (val > mVal)
		if (mRight)
			mRight->insert(val);
		else
			mRight = new Node(val, this);
}

void Node::walk(vector<int> *out)
{
	if (mLeft) mLeft->walk(out);
	out->push_back( mVal );
	if (mRight) mRight->walk(out);
}

int Node::elemCnt()
{
	int res = 1;
	if (mLeft)  res += mLeft->elemCnt();
	if (mRight) res += mRight->elemCnt();

	return res;
}

/* walk and print */
void wprint(Node* n) {
	vector<int> output;
	n->walk(&output);

    for (int i = 0; i < output.size(); i++) {
        cout << output[i] << " ";
    }
    cout << endl;
}

void
showsecs(long msecs)
{
    fprintf(stderr, "%3.5f S\n", ((float)msecs) / 1000.0);
}

int main()
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

    wprint(n);
    n->remove(3);
    wprint(n);
    printf("youpi");
    n->remove(6);
    wprint(n);
    exit(1);

	vector<int> input;
	FILE* fo = fopen("input.txt", "r");
	int cnt, tmp;
	fscanf(fo, "%d", &cnt);
	for (int i = 0; i < cnt; i++) {
		fscanf(fo, "%d", &tmp);
		input.push_back(tmp);
	}

    Chrono chrono;
	n = new Node(input[0]);
	for (int i = 1; i < input.size(); i++) {
		n->insert(input[i]);
	}
    showsecs(chrono.millis());
    chrono.restart();
	
	vector<int> output;
	// output.reserve(n->elemCnt());
	output.reserve(100000);
	n->walk(&output);
    showsecs(chrono.millis());

    // search | remove
    assert( n->search(7298116) ); 
    printf( "%d\n", n->elemCnt() ); 
    n->remove(729811);
    printf( "%d\n", n->elemCnt() ); 

    n->remove(7298116);
    assert( n->elemCnt() == 99 ); 
	
	return 0;
}
