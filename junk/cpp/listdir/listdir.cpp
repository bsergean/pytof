/* vim:set tabstop=4 shiftwidth=4 expandtab: */

#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <stdio.h>

#include <vector>
#include <string>
#include <map>
using namespace std;

void listDir(const char* prefix, vector<string>& files, vector<string>& dirs) 
{
    DIR *d;
	struct dirent *de;
	int killed = 0;

	d = opendir(prefix);
	if (!d) {
		return;
	}

    multimap<size_t, char*> container;

	while (de = readdir(d)) {
        struct stat sb;
        string abspath(prefix);
        abspath += "/";
        abspath += de->d_name;

        stat(abspath.c_str(), &sb);

        size_t modtime = sb.st_mtimespec.tv_sec;
        // printf("%s - %d\n", abspath.c_str(), modtime);

        container.insert(pair<size_t, char*>(modtime, de->d_name));
	}

    for (multimap<size_t, char*>::iterator it = container.begin();
            it != container.end();
            ++it)
    {
       printf("%d %s\n", (*it).first, (*it).second);
    }
}

int main(int argc, char** argv)
{
    vector<string> files, dirs;
    listDir(argv[1], files, dirs);

}
