#include <iostream>
#include <stack>
#include <strings.h>
#include <cassert>

int
toInt(char c)
{
    switch (c) {
        case '0': return 0;
        case '1': return 1;
        case '2': return 2;
        case '3': return 3;
        case '4': return 4;
        case '5': return 5;
        case '6': return 6;
        case '7': return 7;
        case '8': return 8;
        case '9': return 9;
        default:  return -1;
    }
}

int
compute(char input[])
{
    int N = strlen(input);

    std::stack<char> operators;
    std::stack<int> operands;

    for (int i = 0; i < N; ++i) {
        char c = input[i];

        switch (c) {
            case ' ': break;
            case '(': break;
            case '*': operators.push('*'); break;
            case '+': operators.push('+'); break;
            case ')': {
                char op = operators.top();
                operators.pop();

                int a = operands.top();
                operands.pop();
                int b = operands.top();
                operands.pop();

                int val;
                if (op == '+') {
                    val = a + b;
                } else if (op == '*') {
                    val = a * b;
                } else {
                    assert(false);
                }
                operands.push(val);
            } break;
            default: operands.push(toInt(c));
        }
    }

    return operands.top();
}

int
main()
{
    char input[] = "((1 + (1 * 2)) + 2)";
    int res = compute(input);
    std::cout << input << " = " << res << std::endl;
    return 0;
}
