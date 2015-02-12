#include <iostream>
#include <map>
#include <string>
#include <sstream>
#include <limits>
#include <iomanip>

#include <gmp.h>

class BigNum
{
public:
    BigNum();
    BigNum(int n);
    ~BigNum();

    BigNum(const BigNum& other);

    BigNum & operator=(const BigNum &other);

    bool operator==(const BigNum& other) const;
    bool operator< (const BigNum& other) const;

    const BigNum operator+(const BigNum &other) const;
    const BigNum operator-(const BigNum &other) const;

    friend std::ostream& operator<<(std::ostream& os, 
                                    const BigNum& other);

private:
    mpz_t mNum;
};

BigNum::BigNum()
{
    mpz_init_set_si(mNum, 0);
}

BigNum::BigNum(int n)
{
    mpz_init_set_si(mNum, n);
}

BigNum::~BigNum()
{
    mpz_clear(mNum);
}

BigNum::BigNum(const BigNum& other)
{
    mpz_init(mNum);
    mpz_set(mNum, other.mNum);
}

BigNum& 
BigNum::operator=(const BigNum &other)
{
    mpz_init(mNum);
    mpz_set(mNum, other.mNum);
    return *this;
}

bool
BigNum::operator==(const BigNum &other) const
{
    return mpz_cmp(mNum, other.mNum) == 0;
}

bool 
BigNum::operator<(const BigNum& other) const
{
    return mpz_cmp(mNum, other.mNum) < 0;
}

const BigNum 
BigNum::operator+(const BigNum &other) const
{
    BigNum result;
    mpz_add(result.mNum, mNum, other.mNum);
    return result;
}

const BigNum 
BigNum::operator-(const BigNum &other) const
{
    BigNum result;
    mpz_sub(result.mNum, mNum, other.mNum);
    return result;
}

std::ostream& 
operator<<(std::ostream& os, 
           const BigNum& other)
{
    FILE* f = stdout;
    mpz_out_str(f, 10, other.mNum);
    return os;
}

typedef std::pair<BigNum, BigNum> Pair;
typedef std::map<Pair, BigNum> LUT;
LUT lut;

BigNum
robot(BigNum n, BigNum m)
{
    LUT::const_iterator it;
    Pair pair(n, m);
    it = lut.find(pair);
    if (it != lut.end()) {
        return it->second;
    }

    if (n == 1) return 1;
    if (m == 1) return 1;

    BigNum ret = robot(n, m - 1) +
                 robot(n - 1, m);
    lut[pair] = ret;
    return ret;
}

int
main(int argc, char** argv)
{
    if (argc < 3) {
        puts("usage: ./a.out N P");
        return -1;
    }
    int n = atoi(argv[1]);
    int p = atoi(argv[2]);

    std::cout << robot(n, p) << std::endl;
}
