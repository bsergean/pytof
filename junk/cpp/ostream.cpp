#include <iostream>
#include <iterator>
#include <list>

int main() {
    std::list<int> numbers;
    numbers.push_back(1); // = { 1, 2, 3, 4 };
    numbers.push_back(2); // = { 1, 2, 3, 4 };
    numbers.push_back(3); // = { 1, 2, 3, 4 };

    std::copy(numbers.begin(), numbers.end(), 
              std::ostream_iterator<int>(std::cout, " "));
}
