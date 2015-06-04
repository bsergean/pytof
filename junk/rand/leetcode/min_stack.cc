#include <cassert>
#include <stack>
#include <queue>
#include <list>
#include <iostream>

/*

6,3,5,8,1

stack:    6 - 3 - 5 - 8 - 1

minstack: 6 - 3 - 1

Action: Remove 1

stack:    6 - 3 - 5 - 8

minstack: 6 - 3

*/

/*
 * This should be constant time for push and pop, but it fails ...
 * stack is using a deque under the hood.
 */
class MinStackList {
public:
    void push(int x) {
        mStack.push(x);

        if (mMinStack.empty() || (x <= mMinStack.top())) {
            std::cout << "pushing " << x << " into the min stack" << std::endl;
            mMinStack.push(x);
            std::cout << "mMinStack size is now " << mMinStack.size() << std::endl;
        } else {
            std::cout << "not pushing into the min stack" << std::endl;
        }
    }

    void pop() {
        assert(mStack.size() > 0);

        int top = mStack.top();
        mStack.pop();

        if (!mMinStack.empty() && top == mMinStack.top()) {
            std::cout << "popping " << top << " from the min stack" << std::endl;
            mMinStack.pop();
        }
    }

    int top() {
        assert(!mStack.empty());
        return mStack.top();
    }

    int getMin() {
        assert(!mMinStack.empty());
        return mMinStack.top();
    }

private:
#if 0
    std::stack<int, std::list<int> > mStack;
    std::stack<int, std::list<int> > mMinStack;
#else
    std::stack<int> mStack;
    std::stack<int> mMinStack;
#endif
};

/*
 * This should be log(n) for push and pop, since we're using a heap, but
 * succeed !
 */
class MinStackPriorityQueue {
public:
    void push(int x) {
        mStack.push(x);
        mPriorityQueue.push(x);
    }

    void pop() {
        int top = mStack.top();
        mStack.pop();

        if (top == mPriorityQueue.top()) {
            mPriorityQueue.pop();
        }
    }

    int top() {
        return mStack.top();
    }

    int getMin() {
        return mPriorityQueue.top();
    }

private:
    std::stack<int> mStack;
    std::priority_queue<int, 
                        std::vector<int>, 
                        std::greater<int> > mPriorityQueue;
};

void
testCase1()
{
    typedef MinStackList MinStack;
    MinStack stack;

    stack.push(0);
    // 0
    // 0

    stack.push(1);
    // 0 1
    // 0

    stack.push(0),
    // 0 1 0
    // 0 0

    stack.getMin();
    stack.pop();
    stack.getMin();
}

void
testCase2()
{
    typedef MinStackList MinStack;
    MinStack stack;

    int N = 10000;
    for (int i = N; i >= 0; --i) {
        stack.push(i);
        assert(stack.getMin() == i);
    }

    for (int i = N; i >= 0; --i) {
        int top = stack.top();
        assert(stack.getMin() == top);
        stack.pop();
    }
}

int
main()
{
    testCase1();
    return 0;
}
