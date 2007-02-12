
#include <unistd.h>
#include <sys/types.h>
#include <dlfcn.h>
#include <stdio.h>

// dlopen the gl library
// and get glBegin adress

int
main(int argc, char *argv[])
{
  static void *handle;
  char* lib;
  int flags = RTLD_LAZY | RTLD_GLOBAL;
  
  lib = argv[1];

#ifndef _AIX
  // Have to designate the appropriate library member to dlopen 
  // (either shr.o or shr_64.o)
#if defined(__64BIT__)
#define AIXMEMBER "(shr_64.o)"
#else
#define AIXMEMBER "(shr.o)"
#endif

  flags |= RTLD_MEMBER;
  char aixlib[1024];
  if (strlen(lib) > 1000) {
	  fprintf(stderr, "LIB: name too long (%s)\n", lib);
	  abort();
  }
  strcpy(aixlib, lib);
  strcat(aixlib, AIXMEMBER);
  lib = aixlib;
#endif // AIX

  if ((handle = dlopen(lib, flags)) == 0) {
    fprintf(stderr, "Can't attach library %s: %s\n", lib, dlerror());
  } else {
    fprintf(stderr, "library loaded\n");
  }
  

  return 0;
}
