#include <vector>
#include <stack>
#include <iostream>

//
// Op is an operation helper class: 
// record which stack we're poping an element from, 
// and which stack we're pushing an element into.
//
struct Op {
    int pop;
    int push;

    Op(int i, int j): pop(i), push(j) {}

    void flip() {
        int tmp = pop;
        pop = push;
        push = tmp;
    }
};

typedef std::vector<Op> Ops;

//
// Our 3 stacks
//
std::stack<int> s1;
std::stack<int> s2;
std::stack<int> s3;

//
// Push values on the stack. Large block are 
// represented by large entries.
//
void
init(int N)
{
    for (int i = N - 1; i >= 0; --i) {
        s1.push(i);
    }
}

//
// Apply an operation on our 3 stacks
//
void
move(Op op)
{
    int val = -1;
    switch (op.pop) {
        case 1: { val = s1.top(); s1.pop(); } break;
        case 2: { val = s2.top(); s2.pop(); } break;
        case 3: { val = s3.top(); s3.pop(); } break;
    }
    switch (op.push) {
        case 1: { s1.push(val); } break;
        case 2: { s2.push(val); } break;
        case 3: { s3.push(val); } break;
    }
}

//
// Execute a batch of operations
//
void
execute(const Ops& ops)
{
    for (int i = 0; i < ops.size(); ++i) {
        const Op& op = ops[i];
        move(op);
    }
}

// Concatenate 2 list into the input ops list
// what python extend list operation does.
void
extend(Ops& ops, const Ops& copy) 
{
    for (int i = 0; i < copy.size(); ++i) {
        ops.push_back(copy[i]);
    }
}

//
// Reverse a list of operations,
// then flip the operations themselves.
//
void
reverse(Ops& ops)
{
    for (int i = 0; i < ops.size(); ++i) {
        ops[i].flip();
    }

    std::reverse(ops.begin(), ops.end());
}

//
// The main recursive solver.
// Strategy:
//
// 1. Solve the problem for (N-1).
// 2. Move the last element (large disk) to the second
//    empty stack.
// 3. "Un-solve the problem for (N-1), that is move all disk
//    which were on the right-end side / stack 3 back to stack 1.
// 4. Move the large disk to stack 3 which is now clear.
// 5. Move the first stack content to the stack 3, using 
//    the operations from solving at N-1.
//
void
solve(int N, Ops& ops)
{
    if (N == 0) { return; }
    if (N == 1) {
        ops.push_back(Op(1, 3));
        execute(ops);
        return;
    }

    // 1.
    solve(N-1, ops);

    Ops copy(ops); // ops it takes to solve for N-1 

    // 2. Move large one to the middle position
    move(Op(1, 2));
    ops.push_back(Op(1, 2)); // record that move

    // 3. "un-solve", by reversing the moves.
    reverse(copy);
    execute(copy);
    extend(ops, copy);

    // 4. Move large one to the final position
    move(Op(2, 3));
    ops.push_back(Op(2, 3)); // record that move

    // 5. reverse our op list, then execute it.
    reverse(copy);
    execute(copy);
    extend(ops, copy);
}

int
main()
{
    int N = 3;

    init(N);
    Ops ops;
    solve(3, ops);

    for (int i = 0; i < ops.size(); ++i) {
        const Op& op = ops[i];
        std::cout << op.pop << " " << op.push << std::endl;
    }

}
