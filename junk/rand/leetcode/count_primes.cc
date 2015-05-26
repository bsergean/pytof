#include <iostream>
#include <cmath>
#include <vector>

bool
isDivisible(int x, int y)
{
    return (x % y) == 0;
}

namespace naive {

bool 
isPrime(int n)
{
    if (n != 2 && (n % 2) == 0) {
        return false;
    }

    int sqrt = (int) std::sqrt(n);
    for (int i = 2; i < sqrt; ++i) {
        if (isDivisible(n, i)) {
            return false;
        }
    }
    return true;
}

int
countPrimes(int n, std::vector<int>& primes)
{
    int count = 0;

    for (int i = 0; i < n; ++i) {
        if (isPrime(i)) {
            primes.push_back(i);
            count++;
        }
    }

    return count;
}

int
main()
{
    int N = 120;
    std::vector<int> primes(N);
    std::cout << "countPrimes " << countPrimes(N, primes) << std::endl;

    for (int i = 0; i < primes.size(); ++i) {
        std::cout << primes[i] << " ";
    }
    std::cout << std::endl;

    return 0;
}

}

namespace bad_sieves {

bool 
isPrime(int n, std::vector<int>& primes)
{
    int sq = (int) std::sqrt(n);

    for (int i = 0; i < primes.size(); ++i) {
        if (i > sq) break;

        if (isDivisible(n, primes[i])) {
            return false;
        }
    }
    return true;
}

int
countPrimes(
    int n, 
    std::vector<int>& primes,
    std::vector<bool> visited)
{
    primes.push_back(2);
    int k = 2;
    while (k < n) {
        visited[k] = true;
        k += 2;
    }

    for (int i = 3; i < n; ++i) {
        if (visited[i]) continue;

        if (isPrime(i, primes)) {
            primes.push_back(i);

            k = i;
            while (k < n) {
                visited[k] = true;
                k += i;
            }
        }
    }

    return 1 + primes.size();
}

int
main()
{
    int N = 120;
    std::vector<int> primes;

    std::vector<bool> visited(N);
    std::fill(visited.begin(), visited.end(), false);

    std::cout << "countPrimes " << bad_sieves::countPrimes(N, primes, visited) << std::endl;

    for (int i = 0; i < primes.size(); ++i) {
        std::cout << primes[i] << " ";
    }
    std::cout << std::endl;

    return 0;
}

} // namespace

namespace sieves {

int
countPrimes(
    int n,
    std::vector<bool>& primes
)
{
    for (int prime = 2; prime <= n; ++prime) {

        if (!primes[prime]) continue;

        int k = prime * prime; // can yield to int overflow !!
        while (k < n) {
            primes[k] = false;
            k += prime;
        }
    }

    int count = 0;
    for (int i = 2; i < primes.size(); ++i) {
        if (primes[i]) {
            count++;
        }
    }

    return count;
}

int
main()
{
    int N = 100000;
    std::vector<bool> primes(N);
    std::fill(primes.begin(), primes.end(), true);

    std::cout << "countPrimes " << sieves::countPrimes(N, primes) << std::endl;

    for (int i = 2; i < primes.size(); ++i) {
        if (primes[i]) {
            std::cout << i << " ";
        }
    }
    std::cout << std::endl;

    return 0;
}

}

int 
main()
{
    // naive::main();
    // bad_sieves::main();
    sieves::main();
}

