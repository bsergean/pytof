
#include <assert.h>
#include <string>
#include <vector>
using namespace std;

void split(const string& in, int sep, vector<string>& sList)
{
	sList.clear();

	string token;
        size_t start = 0;
        size_t end;
        while ((end = in.find(sep, start)) != string::npos) {
		token = in.substr(start, end - start);
                sList.push_back(token);
		printf("new token \"%s\"\n", token.c_str());
                start = end + 1;
        }
	token = in.substr(start);
	sList.push_back(token);
	printf("new token \"%s\"\n", token.c_str());

	puts("Done");
}

int main()
{
	vector<string> V;
	string in;
	
	in = ("foo.bar");
	split(in, '.', V);

	assert( V[0] == string("foo") );
	assert( V[1] == string("bar") );

	in = ("..");
	split(in, '.', V);

	assert( V[0] == string("") );
	assert( V[1] == string("") );
}
