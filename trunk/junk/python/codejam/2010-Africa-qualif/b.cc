#include <iostream>
#include <sstream>
#include <vector>
#include <string>

void
reverse(std::vector<std::string>& V)
{
    int N = V.size();
    for (int i = 0; i < N/2; ++i) {
        std::string copy = V[i];
        V[i]     = V[N-i-1];
        V[N-i-1] = copy;
    }
}

int
main()
{
    int N;
    std::cin >> N;
    // std::cout << N << " datasets" << std::endl;

    // Get the end of the first line.
    std::string foo;
    std::getline(std::cin, foo);
    
    for (int d = 0; d < N; ++d) {
        std::string line;
        std::getline(std::cin, line);

        std::stringstream ss;
        ss << line;
        std::vector<std::string> items;
        while (ss) {
            std::string temp;
            ss >> temp;
            items.push_back(temp);
        }

#if 0
        std::reverse(items.begin(), items.end());
#else
        reverse(items);
#endif
        std::cout << "Case #" << d+1 << ": ";
        for (int i = 0; i < items.size(); ++i) {
            std::cout << items[i] << " ";
        }
        std::cout << std::endl;
    }
}
