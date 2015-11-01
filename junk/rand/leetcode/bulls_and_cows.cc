
#include <string>
#include <iostream>
#include <sstream>
#include <cassert>
#include <vector>
#include <map>
#include <unordered_map>

std::string
getHintBad(std::string secret, std::string guess) 
{
    int bulls, cows;
    bulls = 0;
    cows = 0;

    int N = secret.size();

    std::vector<bool> bullFound(N, false);

    for (int i = 0; i < N; ++i) {
        if (secret[i] == guess[i]) {
            bulls += 1;
            bullFound[i] = true;

            secret[i] = 'A';
        }
    }

    for (int i = 0; i < N; ++i) {

        if (bullFound[i]) continue;

        char potentialSecretChar = guess[i];

        for (int j = 0; j < N; ++j) {

            if (i != j && 
                potentialSecretChar == secret[j] && 
                !bullFound[j]) {

                secret[j] = 'B';
                cows += 1;
            }
        }
    }

    // std::cout << "\nupdated secret: " << secret << "\n";

    std::stringstream ss;
    ss << bulls;
    ss << "A";
    ss << cows;
    ss << "B";
    return ss.str();
}

std::string
getHint(std::string secret, std::string guess) 
{
    typedef std::unordered_map<char, int> Histogram;
    typedef std::unordered_map<char, int>::iterator HistogramIterator;

    int bulls, cows;
    bulls = 0;
    cows = 0;

    Histogram secretHistogram, guessHistogram;

    int N = secret.size();

    for (int i = 0; i < N; ++i) {
        char s = secret[i];
        char g = guess[i];
        if (s == g) {
            bulls += 1;
        } else {
            HistogramIterator it;

            it = secretHistogram.find(s);
            if (it == secretHistogram.end()) {
                secretHistogram[s] = 1;
            } else {
                secretHistogram[s]++;
            }

            it = guessHistogram.find(g);
            if (it == guessHistogram.end()) {
                guessHistogram[g] = 1;
            } else {
                guessHistogram[g]++;
            }
        }
    }

    HistogramIterator it, itEnd;
    it    = guessHistogram.begin();
    itEnd = guessHistogram.end();

    for (; it != itEnd; ++it) {
        HistogramIterator jt;

        jt = secretHistogram.find(it->first);
        if (jt != secretHistogram.end()) {
            cows += std::min(it->second, jt->second);
        }
    }

    // std::cout << "\nupdated secret: " << secret << "\n";

    std::stringstream ss;
    ss << bulls;
    ss << "A";
    ss << cows;
    ss << "B";
    return ss.str();
}

int
main()
{
    std::string secret, guess;

    secret = "1807";
    guess  = "7810";
    std::cout << "secret: " << secret << "\n"
              << "guess:  " << guess  << "\n"
              << "hint:   " << getHint(secret, guess) << "\n\n";
    assert(getHint(secret, guess) == "1A3B");

    secret = "1";
    guess  = "1";
    std::cout << "secret: " << secret << "\n"
              << "guess:  " << guess  << "\n"
              << "hint:   " << getHint(secret, guess) << "\n\n";
    assert(getHint(secret, guess) == "1A0B");

    secret = "11";
    guess  = "10";
    std::cout << "secret: " << secret << "\n"
              << "guess:  " << guess  << "\n"
              << "hint:   " << getHint(secret, guess) << "\n\n";
    assert(getHint(secret, guess) == "1A0B");

    secret = "011";
    guess  = "110";
    std::cout << "secret: " << secret << "\n"
              << "guess:  " << guess  << "\n"
              << "hint:   " << getHint(secret, guess) << "\n\n";
    assert(getHint(secret, guess) == "1A2B");

    secret = "1234";
    guess  = "0111";
    std::cout << "secret: " << secret << "\n"
              << "guess:  " << guess  << "\n"
              << "hint:   " << getHint(secret, guess) << "\n\n";
    assert(getHint(secret, guess) == "0A1B");

    secret = "1122";
    guess  = "0001";
    std::cout << "secret: " << secret << "\n"
              << "guess:  " << guess  << "\n"
              << "hint:   " << getHint(secret, guess) << "\n\n";
    assert(getHint(secret, guess) == "0A1B");

    secret = "1122";
    guess  = "2211";
    std::cout << "secret: " << secret << "\n"
              << "guess:  " << guess  << "\n"
              << "hint:   " << getHint(secret, guess) << "\n\n";
    assert(getHint(secret, guess) == "0A4B");

    return 0;
}
