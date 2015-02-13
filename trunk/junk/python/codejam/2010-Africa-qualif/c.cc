#include <iostream>
#include <sstream>
#include <vector>
#include <string>

int
main()
{
    int N;
    std::cin >> N;

    // Get the end of the first line.
    std::string foo;
    std::getline(std::cin, foo);
    
    for (int d = 0; d < N; ++d) {
        std::string line;
        std::getline(std::cin, line);

        std::cout << "Case #" << d+1 << ": ";

        int lastKey = -1; // special char
        int key = -1;

        for (int i = 0; i < line.size(); ++i) {

            char c = line[i];
            std::string out;

            if (c == ' ') { key = 0; out = "0"; }

            if (c == 'a') { key = 2; out = "2"; }
            if (c == 'b') { key = 2; out = "22"; }
            if (c == 'c') { key = 2; out = "222"; }

            if (c == 'd') { key = 3; out = "3"; }
            if (c == 'e') { key = 3; out = "33"; }
            if (c == 'f') { key = 3; out = "333"; }

            if (c == 'g') { key = 4; out = "4"; }
            if (c == 'h') { key = 4; out = "44"; }
            if (c == 'i') { key = 4; out = "444"; }

            if (c == 'j') { key = 5; out = "5"; }
            if (c == 'k') { key = 5; out = "55"; }
            if (c == 'l') { key = 5; out = "555"; }

            if (c == 'm') { key = 6; out = "6"; }
            if (c == 'n') { key = 6; out = "66"; }
            if (c == 'o') { key = 6; out = "666"; }

            if (c == 'p') { key = 7; out = "7"; }
            if (c == 'q') { key = 7; out = "77"; }
            if (c == 'r') { key = 7; out = "777"; }
            if (c == 's') { key = 7; out = "7777"; }

            if (c == 't') { key = 8; out = "8"; }
            if (c == 'u') { key = 8; out = "88"; }
            if (c == 'v') { key = 8; out = "888"; }

            if (c == 'w') { key = 9; out = "9"; }
            if (c == 'x') { key = 9; out = "99"; }
            if (c == 'y') { key = 9; out = "999"; }
            if (c == 'z') { key = 9; out = "9999"; }

            if (key == lastKey) {
                std::cout << " ";
            }
            lastKey = key;

            std::cout << out;
        }

        std::cout << std::endl;
    }
}
