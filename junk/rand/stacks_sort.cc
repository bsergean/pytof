#include <iostream>
#include <stack>

typedef std::stack<int> Stack;

Stack
sort(Stack stack)
{
    Stack output;

    while (!stack.empty()) {
        int top = stack.top();
        stack.pop();

        // insert top in sorted output 
        while (!output.empty()) {
            int tmp = output.top();
            if (tmp > top) {
                output.pop();
                stack.push(tmp);
            } else {
                break;
            }
        }

        output.push(top);
    }

    return output;
}

int 
main()
{
    std::stack<int> stack;

    stack.push(3);
    stack.push(1);
    stack.push(2);
    stack.push(9);
    stack.push(5);
    stack.push(6);

    std::stack<int> sortedStack = sort(stack);
    std::cout << "size = " << sortedStack.size() << std::endl;

    while (!sortedStack.empty()) {
        int top = sortedStack.top();
        sortedStack.pop();
        std::cout << top << " ";
    }

    std::cout << std::endl;
}
