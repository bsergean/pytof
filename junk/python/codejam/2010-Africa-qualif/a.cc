#include <iostream>
#include <vector>
#include <string>

int
main()
{
    int N;
    std::cin >> N;
    // std::cout << N << " datasets" << std::endl;
    
    for (int d = 0; d < N; ++d) {
        int C;
        std::cin >> C;

        std::vector<int> items;
        int l;
        std::cin >> l;
        for (int j = 0; j < l; ++j) {
            int temp;
            std::cin >> temp;
            items.push_back(temp);
        }

        for (int i = 0; i < l; ++i) {
            for (int j = i + 1; j < l; ++j) {
                if (items[i] + items[j] == C) {
                    std::cout << "Case #" << d+1 << ": "
                              << i+1 << " " << j+1 << std::endl;
                }
            }
        }

        // for (int i = 0; i < items.size(); ++i) {
        //     std::cout << items[i] << " ";
        // }
        // std::cout << std::endl;
    }
}
