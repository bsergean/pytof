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

void find(const char* prefix) 
{
    puts(prefix);

    DIR *d;
	struct dirent *de;

	d = opendir(prefix);
	if (!d) {
		return;
	}

    int i = 0;
	while (de = readdir(d)) {
        if (i < 2) {
            i++;
            continue;
        }

        string abspath(prefix);
        abspath += "/";
        abspath += de->d_name;
        const char* absp = abspath.c_str();

        if ( de->d_type == DT_DIR ) {
            find(absp);
        } else if ( de->d_type == DT_DIR ) {
            puts(absp);
        }
    }

    closedir(d);
}

int main(int argc, char** argv)
{
    vector<string> files, dirs;
    // listDir(argv[1], files, dirs);

    find(argv[1]);
}
