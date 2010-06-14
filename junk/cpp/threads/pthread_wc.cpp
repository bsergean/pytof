
/* https://computing.llnl.gov/tutorials/pthreads/ */

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

#include <string>
using std::string;

/*
 * find ~/src/pytof -name '*.py' -o -name '*.cpp' | /usr/bin/time xargs wc -l
 */

void *lc(void *fn_void)
{
   char* fn = (char*) fn_void;
   struct stat st;
   stat(fn, & st);

   char* buffer = new char[st.st_size];
   FILE* fo = fopen(fn, "r");
   fread(buffer, 1, st.st_size, fo);
   string in(buffer);
   delete [] buffer;

   size_t start = 0;
   size_t end;
   int lines = 0;
   while ((end = in.find('\n', start)) != string::npos) {
	   lines += 1;
	   start = end + 1;
   }

   fclose(fo);
   printf("%s: %d lines\n", fn, lines);
   pthread_exit(NULL);
}

int main (int argc, char *argv[])
{
   pthread_t threads[argc];
   int rc;
   long t;
   for(unsigned t = 1; t < argc; t++){
      printf("In main: creating thread %d\n", t);
      rc = pthread_create(&threads[t], NULL, lc, (void *) argv[t]);
      if (rc){
         printf("ERROR; return code from pthread_create() is %d\n", rc);
         exit(-1);
      }
   }
   pthread_exit(NULL);
}

