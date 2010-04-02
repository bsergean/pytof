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
        } else {
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
        /*
        size_t E = strlen(de->d_name);
        size_t S = P + E + 2;
        char* absp = (char*) alloca(P + E + 2);
        memcpy(absp, prefix, P);
        absp[P] = '/';
        memcpy(absp + P + 1, de->d_name, E);
        absp[S-1] = '\0';
        */

        if ( de->d_type == DT_DIR ) {
            size_t E = strlen(de->d_name);
            size_t S = P + E + 2;
            char* absp = (char*) alloca(S);

            sprintf(absp, "%s/%s", prefix, de->d_name);
            find2(absp);
        } else {
            // puts(absp);
            printf("%s/%s\n", prefix, de->d_name);
        }
    }

    closedir(d);
}

// BUGGY
void find3(const char* prefix) 
{
    puts(prefix);

	DIR* d = opendir(prefix);
	if (!d) return;

    /* Those two guys for . and .. */
	struct dirent *de = readdir(d);
	de = readdir(d);

    size_t P = strlen(prefix);
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
            printf("%s/%s\n", prefix, de->d_name);
        }
    }

    closedir(d);
}

// BUGGY
void find4(const char* prefix) 
{
    puts(prefix);

	DIR* d = opendir(prefix);
	if (!d) return;

    /* Those two guys for . and .. */
	struct dirent *de = readdir(d);
	de = readdir(d);

	while (de = readdir(d)) {
        if ( de->d_type == DT_DIR ) {
            static char path[1024];
            sprintf(path, "%s/%s", prefix, de->d_name);

            find4(path);
        } else if ( de->d_type == DT_REG ) {
            printf("%s/%s\n", prefix, de->d_name);
        }
    }

    closedir(d);
}

void find5_rec(const char* prefix) 
{
    puts(prefix);

	DIR* d = opendir(".");
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
            chdir(de->d_name);
            find5_rec(absp);
            chdir("..");
        } else if ( de->d_type == DT_REG ) {
            puts(absp);
        }

        // free mem if you use alloca instead of malloc
        // free(absp);
    }

    closedir(d);
}

void find5(const char* prefix) 
{
    chdir(prefix);
    find5_rec(prefix);
}

void find6(char* buffer, int cur)
{
  puts(buffer);
  DIR* dir = opendir(buffer);
  if (dir) {
    buffer[cur++] = '/';
    readdir(dir);  // .
    readdir(dir);  // ..
    while (struct dirent* entry = readdir(dir)) {
      strcpy(buffer + cur, entry->d_name);
      find6(buffer, cur + strlen(entry->d_name));
      buffer[cur] = 0;
    }
  }
  if (dir)
      closedir(dir);
}

int main(int argc, char** argv)
{
#if 1
    // setbuf(stdout, _IOFBF);
    find2(argv[1]);
#else
    char buffer[640 << 10];  // That should be enough.
    find6(strcpy(buffer, argv[1]), strlen(argv[1]));
#endif
}
