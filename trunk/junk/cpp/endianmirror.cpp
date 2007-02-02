#include <stdio.h>
#include <string>

using namespace std;

char* file2buffer(string filename, int* bufferSize)
{
  char* buffer;
  FILE* fin;
  
  if (! (fin = fopen(filename.c_str(), "r")) )
    return NULL;
  
  fseek(fin, 0, SEEK_END);
  *bufferSize = ftell(fin);
  fseek(fin, 0, SEEK_SET);

  if (*bufferSize == 0)
    return NULL;
  
  fprintf(stderr,"%d char in %s\n", *bufferSize, filename.c_str());
  buffer = (char*) malloc(*bufferSize * sizeof(char));
  
  if (!buffer)
    {
      return NULL;
    }

  memset(buffer, 0, *bufferSize);
  fread(buffer, 1, *bufferSize, fin);
  fclose(fin);

  return buffer;
}

int main(int argc, char** argv)
{
  if (argc != 3)
    {
      fprintf(stderr, "usage: endianmirror <in> <out>");
      exit(0);
    }
  
  string in(argv[1]);
  string out(argv[2]);

  int bufferSize;
  char* iBuffer = file2buffer(in, &bufferSize);
  FILE* fo = fopen(out.c_str(), "w");

  for (int i = 0; i < bufferSize; i += 4)
    fprintf(fo, "%c%c%c%c",
	    iBuffer[i+3],
	    iBuffer[i+2],
	    iBuffer[i+1],
	    iBuffer[i]);

  return 0;
}
