/* vim:set tabstop=4 shiftwidth=4 expandtab: */

#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <stdio.h>

#include <vector>
#include <string>
#include <map>
#include <iostream>
using namespace std;

void 
listDirs(
    const char* prefix, 
    vector<string>& dirs
)
{
    DIR *d;
	struct dirent *de;
	int killed = 0;

	d = opendir(prefix);
	if (!d) {
        std::cerr << "cannot opendir " << prefix << "\n";
		return;
	}

    int i = 0;
	while ((de = readdir(d))) {
        if (i < 2) {
            i++;
            continue;
        }
    
        struct stat sb;
        string abspath(prefix);
        abspath += "/";
        abspath += de->d_name;

        dirs.push_back(abspath);
	}
}

void* 
listFiles(
    void* input
)
{
    const char* prefix = (const char*) input;
    // printf("listFiles %s\n", prefix);
    DIR *d;
	struct dirent *de;

	d = opendir(prefix);
	if (!d) {
		return NULL;
	}

    int i = 0;
	while ((de = readdir(d))) {
        if (i < 2) {
            i++;
            continue;
        }

        struct stat sb;
        string abspath(prefix);
        abspath += "/";
        abspath += de->d_name;

        stat(abspath.c_str(), &sb);

        size_t modtime = sb.st_mtimespec.tv_sec;
        printf("%s - %ld\n", abspath.c_str(), modtime);
	}

    pthread_exit(NULL);
    return NULL;
}

void 
listLogFiles(
    const char* prefix
)
{
    vector<string> dirs;
    listDirs(prefix, dirs);

    bool threaded = true;

    if (!threaded) {
        for (unsigned i = 0; i < dirs.size(); ++i) {
            listFiles((void*) dirs[i].c_str());
        }
    } else {
        unsigned threadCount = dirs.size();
        pthread_t threads[threadCount];

        for (unsigned i = 0; i < dirs.size(); ++i) {
            int rc = pthread_create(&threads[i], NULL, 
                                    listFiles, (void *) dirs[i].c_str());
            if (rc) {
                printf("ERROR; return code from pthread_create() is %d\n",
                       rc);
                exit(-1);
            }
        }        

       /* Last thing that main() should do */
       pthread_exit(NULL);
    }
}

int main(int argc, char** argv)
{
    listLogFiles(argv[1]);
}
