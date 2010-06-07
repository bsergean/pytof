#include <regex.h>
#include <pcre.h>

#include <vector>
#include <string>
using namespace std;

// http://en.wikipedia.org/wiki/Regular_expression#POSIX_character_classes
class Regexp
{
public:
	Regexp(string re, unsigned groupCount=1);
	~Regexp();
	bool match(const string& in);

	vector<string> groups;

private:
	regex_t *regpattern;
	string mRe;
	unsigned mGroupCount;
};

Regexp::Regexp(string re, unsigned groupCount)
{
	mRe = re;

	if (groupCount < 1) mGroupCount = 1;
	else mGroupCount = groupCount + 1;

        char *pattern = const_cast<char*>(re.c_str());
	regpattern = new regex_t;

	if (regcomp(regpattern, pattern, REG_EXTENDED)) {
		puts("invalid pattern");
		delete regpattern;
	}
}

Regexp::~Regexp()
{
	regfree(regpattern);
}

bool Regexp::match(const string& in)
{
	groups.clear();

	regmatch_t* rm = new regmatch_t[mGroupCount];
	// regmatch_t* rm = (regmatch_t*) malloc(mGroupCount * sizeof(regmatch_t));
	bool matched = regexec(regpattern, in.c_str(), mGroupCount, rm, 0) == 0;

	printf("%s match %s ? %d\n", in.c_str(), mRe.c_str(), matched);

	if (matched) {
		for (unsigned i = 0; i < mGroupCount; ++i) {
			printf("match %d %d\n", rm[i].rm_so, rm[i].rm_eo);
			int begin = rm[i].rm_so;
			int end = rm[i].rm_eo;
			if (begin != -1 && end != -1) {
				string group( in.substr(begin, end - 1) );
				printf("group[%d] = %s\n", i, group.c_str());
				groups.push_back( group );
			}
		}
	}

	delete [] rm;
	return matched;
}

int main()
{
	// Regexp re("[:digit:]");
	bool res;
	Regexp re("ab");

	res = re.match("AAAAac");
	res = re.match("AAAAab");

	Regexp re1("toto([0-9]*)", 1);
	if ( re1.match("toto2000") ) {
		printf("group 1: %s\n", re1.groups[1].c_str());
	}

	// >>> re.match(r'^(.*)\.([0-9]*)\.([0-9]*)\.(.*)$', 'foo.100.5.mm').groups()
	// ('foo', '100', '5', 'mm')

	Regexp re2("(.*)\\.([0-9]*)\\.([0-9]*)\\.(.*)$", 4);
	if ( re2.match("foo.100.5.mm") ) {
		printf("group 1: %s\n", re2.groups[1].c_str());
	}
}
