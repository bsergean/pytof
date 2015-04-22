#include <string>
#include <sstream>
#include <iostream>
#include <stdio.h>
#include <cassert>

void
compress(char* s, std::string& out)
{
    // error handling
    if (s == NULL) {
        out.clear();
        return;
    }

    int N = strlen(s);

    if (N == 0) {
        out.clear();
        return;
    }

    int total = 0;
    int count = 1;
    char prev = s[0];
    char curr;

    std::string numberAsString;

    for (int i = 1; i < N; ++i) {
        curr = s[i];
        if (curr == prev) {
            count++;
        } else {
            out.push_back(prev);
            std::stringstream ss;
            ss << count;
            numberAsString = ss.str();
            std::cout << "number as string for '" << prev << "' = " << numberAsString << std::endl;
            out += numberAsString;
            count = 1;
            prev = curr;

            total += 1; // char
            total += numberAsString.size(); // count
        }
    }

    out.push_back(prev);
    std::stringstream ss;
    ss << count;
    numberAsString = ss.str();
    std::cout << "number as string for '" << prev << "' = " << numberAsString << std::endl;
    out += numberAsString;
    count = 1;
    prev = curr;

    total += 1; // char
    total += numberAsString.size(); // count

    return;

    if (total < N) {
        out.clear();
        out = s;
    }
}

int main()
{
    char input[] = "aabccccca";
    std::string out;
    compress(input, out);
    printf("%s\n", out.c_str());
}
