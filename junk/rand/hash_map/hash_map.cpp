#include <stdio.h>
#include <strings.h>
#include <assert.h>
#include <stdint.h>

//
// FIXME / bring back timers to compare performances
//

// Cool article about memoization and dynamic programming 
// http://marknelson.us/2007/08/01/memoization/

// The black magic to use g++ hash_map
// http://gcc.gnu.org/ml/libstdc++/2002-04/msg00107.html
#include <ext/hash_map>
using namespace __gnu_cxx;
#include <string>
#include <ext/hash_map>

namespace __gnu_cxx
{
        template<> struct hash< std::string >
        {
                size_t operator()( const std::string& x ) const
                {
                        return hash< const char* >()( x.c_str() );
                }
        };
}
// 

// Could not make this one work :)
// #include <tr1/unordered_map>
// using namespace std::tr1;

#include <map>
#include <vector>
#include <list>
#include <string>
using namespace std;

extern unsigned int MurmurHash2 ( const void * key, int len, unsigned int seed );
extern uint64_t MurmurHash64A ( const void * key, int len, unsigned int seed );

#define _S_num_primes 28

static const unsigned long stl_prime_list[_S_num_primes] =
{
	53ul,         97ul,         193ul,       389ul,       769ul,
	1543ul,       3079ul,       6151ul,      12289ul,     24593ul,
	49157ul,      98317ul,      196613ul,    393241ul,    786433ul,
	1572869ul,    3145739ul,    6291469ul,   12582917ul,  25165843ul,
	50331653ul,   100663319ul,  201326611ul, 402653189ul, 805306457ul,
	1610612741ul, 3221225473ul, 4294967291ul
};

unsigned long
stl_next_prime(unsigned long __n)
{
	const unsigned long* __first = stl_prime_list;
	const unsigned long* __last = stl_prime_list + (int)_S_num_primes;
	const unsigned long* pos = std::lower_bound(__first, __last, __n);
	return pos == __last ? *(__last - 1) : *pos;
}

class HashMap
{
public:
	HashMap(int size);
	void insert(const std::string& key, int value);
	int get(const std::string& key) const;
	void print() const;

private:
    int hash(const string& key) const;

    std::vector< std::list< std::pair<string, int> > > mTable;
};

HashMap::HashMap(int size) 
{
    printf("New hash map with %d elems\n", size);
    int bucket_cnt = stl_next_prime(size);
    mTable.resize(bucket_cnt);
}

int 
HashMap::hash(const string& key) const
{
    // The hash I remember from school is terrible 
    // for dictionary strings
#if 0
    int res = 0;
    for (int i = 0; i < key.length(); i++) res += key[i];
    return res % mTable.size();
#endif

    int res = MurmurHash2(key.c_str(), key.length(), 0);
    return res % mTable.size();

#if 0
    uint64_t res = MurmurHash64A( key.c_str(), key.length(), 0);
#endif

#if 0
    unsigned long __h = 0;
    const char* __s = key.c_str();
    for ( ; *__s; ++__s) {
        __h = 5 * __h + *__s;
    }

    return __h % mTable.size();
#endif
}

void 
HashMap::insert(const std::string& key, int value) 
{
    int row = hash(key);
    mTable[row].push_back(pair<std::string, int>(key, value));
}

int 
HashMap::get(const std::string& key) const
{
    int row = hash(key);
    list< pair<string, int> >::const_iterator it, itEnd;

    it    = mTable[row].begin();
    itEnd = mTable[row].end();

    for (; it != itEnd; ++it) {
        if (key == it->first) {
            return it->second;
        }
    }

    return -1;
}

void 
HashMap::print() const
{
    for (int i = 0; i < mTable.size(); i++) {
        printf("%zu ", mTable[i].size());
        list< pair<string, int> >::const_iterator it;

        for (it = mTable[i].begin(); it != mTable[i].end(); it++) {
            printf("%s %d ", 
                   it->first.c_str(), it->second);
        }
        puts("");
    }
}

int main()
{
	FILE *fd;
	char line[100];
	vector<string> V;

	fd = fopen ("/usr/share/dict/words", "r");
	while (fgets (line , 100 , fd)) {
		size_t L = strlen(line);
		line[L-1] = 0;
		// puts (line);

		V.push_back(line);
		// M[line] = true;
	}
	fclose (fd);

	//
	// STL Map
	//
	puts("STL Map");
	map<string, int> M;
	map<string, int>::iterator it;

	// Insertion
	for (int i = 0; i < V.size(); i++) {
		M[ V[i] ] = V[i].length();
	}

	// Search
	for (int i = 0; i < V.size(); i++) {
		// puts(V[i].c_str());

		it = M.find( V[i] );
		assert( it != M.end() );
	}
	
	//
	// STL GNU hash map
	//
	puts("STL GNU hash map");
	hash_map<string, int> HM;
	hash_map<string, int>::iterator hm_it;

	// Insertion
	for (int i = 0; i < V.size(); i++) {
		HM[ V[i] ] = V[i].length();
	}

	// Search
	for (int i = 0; i < V.size(); i++) {
		// puts(V[i].c_str());

		hm_it = HM.find( V[i] );
		assert( hm_it != HM.end() );
	}

	//
	// Ben Map
	//
	puts("Ben hash map");
	HashMap hm(V.size());

	// Insertion
	for (int i = 0; i < V.size(); i++) {
		hm.insert( V[i], V[i].size() );
	}

	// hm.print();

	// Search
	for (int i = 0; i < V.size(); i++) {
		// puts(V[i].c_str());

		int val = hm.get( V[i] );
		assert( val != -1 );
	}

	return 0;
}
