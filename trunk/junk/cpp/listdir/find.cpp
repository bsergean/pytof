/* vim:set tabstop=4 shiftwidth=4 expandtab: */

#include <sys/types.h>
#include <dirent.h>
#include <stdio.h>
#include <alloca.h>

#include <string>
using std::string;

void find1(const char* prefix) 
{
    puts(prefix);

	DIR* d = opendir(prefix);
	if (!d) return;

    /* Those two guys for . and .. */
	struct dirent *de = readdir(d);
	de = readdir(d);

	while (de = readdir(d)) {
        string abspath(prefix);
        abspath += "/";
        abspath += de->d_name;
        const char* absp = abspath.c_str();

        if ( de->d_type == DT_DIR ) {
            find1(absp);
        } else if ( de->d_type == DT_REG ) {
            puts(absp);
        }

        // free mem if you use alloca instead of malloc
        // free(absp);
    }

    closedir(d);
}

void find2(const char* prefix) 
{
    puts(prefix);

	DIR* d = opendir(prefix);
	if (!d) return;

    /* Those two guys for . and .. */
	struct dirent *de = readdir(d);
	de = readdir(d);

    size_t P = strlen(prefix);
	while (de = readdir(d)) {
        size_t E = strlen(de->d_name);
        size_t S = P + E + 2;
        char* absp = (char*) alloca(P + E + 2);
        memcpy(absp, prefix, P);
        absp[P] = '/';
        memcpy(absp + P + 1, de->d_name, E);
        absp[S-1] = '\0';

        if ( de->d_type == DT_DIR ) {
            find2(absp);
        } else if ( de->d_type == DT_REG ) {
            puts(absp);
        }
    }

    closedir(d);
}

void find3(const char* prefix) 
{
    puts(prefix);

	DIR* d = opendir(prefix);
	if (!d) return;

    /* Those two guys for . and .. */
	struct dirent *de = readdir(d);
	de = readdir(d);

    char filepath[1024];
    size_t P = strlen(prefix);
    memcpy(filepath, prefix, strlen(prefix));
    filepath[P] = '/';

	while (de = readdir(d)) {
        if ( de->d_type == DT_DIR ) {
            size_t E = strlen(de->d_name);
            size_t S = P + E + 2;
            char* absp = (char*) alloca(P + E + 2);
            memcpy(absp, prefix, P);
            absp[P] = '/';
            memcpy(absp + P + 1, de->d_name, E);
            absp[S-1] = '\0';

            find3(absp);
        } else if ( de->d_type == DT_REG ) {
            printf("%s/", prefix);
            size_t E = strlen(de->d_name);
            memcpy(filepath + P + 1, de->d_name, E);
            filepath[P + E + 1] = '\0';
            puts(filepath);
        }
    }

    closedir(d);
}

int main(int argc, char** argv)
{
    find3(argv[1]);
}
