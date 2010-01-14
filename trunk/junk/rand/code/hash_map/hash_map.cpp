#include <stdio.h>
#include <strings.h>
#include <assert.h>
#include <stdint.h>

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

#include "chrono.h"

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
	HashMap(int size) {
		printf("New hash map with %d elems\n", size);
		int bucket_cnt = stl_next_prime(size);
		m_table.resize(bucket_cnt);
	}

	int hash(string key) {
		/*
		 * The hash I remember from school is terrible 
		 * for dictionary strings
		int res = 0;
		for (int i = 0; i < key.length(); i++) res += key[i];
		return res % m_table.size();
		*/

		/*
		int res = MurmurHash2( key.c_str(), key.length(), 0);
		return res % m_table.size();
		uint64_t res = MurmurHash64A( key.c_str(), key.length(), 0);
		*/

		unsigned long __h = 0;
		const char* __s = key.c_str();
		for ( ; *__s; ++__s)
			__h = 5 * __h + *__s;

		return __h % m_table.size();
	}

	void insert(string key, int value) {
		// printf("Insert %s - %d\n", key.c_str(), value);
		int row = hash(key);
		// printf("row: %d\n", row);
		pair<string, int> p(key, value);
		m_table[row].push_back(p);
	}

	int get(string key) {
		// printf("Insert %s - %d\n", key.c_str(), value);
		int row = hash(key);
		// printf("row: %d\n", row);

		list< pair<string, int> >::const_iterator it;
		for (	it = m_table[row].begin();
			it != m_table[row].end();
			it++) {
			if (key == it->first)
				return it->second;
		}
		return -1;
	}

	void print() {
		for (int i = 0; i < m_table.size(); i++)
		{
			printf("%d ", m_table[i].size());
			list< pair<string, int> >::const_iterator it;
			for (	it = m_table[i].begin();
				it != m_table[i].end();
				it++) {
				("");
				printf("%s %d ", 
					it->first.c_str(), 
					it->second);
			}
			puts("");
		}
	}

private:
	vector< list< pair<string, int> > > m_table;
};

void
showsecs(long msecs)
{
    fprintf(stderr, "%3.5f S\n", ((float)msecs) / 1000.0);
}

int main()
{
	FILE *fd;
	char line[100];
	vector<string> V;
	Chrono chrono;

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
	chrono.restart();
	map<string, int> M;
	map<string, int>::iterator it;

	// Insertion
	for (int i = 0; i < V.size(); i++)
	{
		M[ V[i] ] = V[i].length();
	}
	showsecs(chrono.millis());

	chrono.restart();
	// Search
	for (int i = 0; i < V.size(); i++)
	{
		// puts(V[i].c_str());

		it = M.find( V[i] );
		assert( it != M.end() );
	}
	showsecs(chrono.millis());
	
	//
	// STL GNU hash map
	//
	puts("STL GNU hash map");
	chrono.restart();
	hash_map<string, int> HM;
	hash_map<string, int>::iterator hm_it;

	// Insertion
	for (int i = 0; i < V.size(); i++)
	{
		HM[ V[i] ] = V[i].length();
	}
	showsecs(chrono.millis());

	chrono.restart();
	// Search
	for (int i = 0; i < V.size(); i++)
	{
		// puts(V[i].c_str());

		hm_it = HM.find( V[i] );
		assert( hm_it != HM.end() );
	}
	showsecs(chrono.millis());

	//
	// Ben Map
	//
	puts("Ben hash map");
	chrono.restart();
	HashMap hm(V.size());

	// Insertion
	for (int i = 0; i < V.size(); i++)
	{
		hm.insert( V[i], V[i].size() );
	}
	showsecs(chrono.millis());

	// hm.print();

	chrono.restart();
	// Search
	for (int i = 0; i < V.size(); i++)
	{
		// puts(V[i].c_str());

		int val = hm.get( V[i] );
		assert( val != -1 );
	}
	showsecs(chrono.millis());

	return 0;
}
