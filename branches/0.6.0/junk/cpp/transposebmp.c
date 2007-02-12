#include <stdio.h>
#include <zlib.h>

FILE* g_fout;
static char* file2buffer(const char* filename, int* bufferSize);
static void transposebmp(const char* input_filename);

/* HARDCODED */
const unsigned int bmpwidth = 500;
const unsigned int bmpheight = 400;

static char usage [] =
"usage : transposebmp <file>\n"
"generate /tmp/transposed.bmp\n"
""
;

int main(int argc, char** argv)
{
  if (argc == 2)
    {
      transposebmp(argv[1]);
    }
  else
    {
      puts(usage);
    }
  return 0;
}

static char* file2buffer(const char* filename, int* bufferSize)
{
  char c;
  int i = 0;
  char* buffer;
  FILE* fin = fopen(filename, "r");

  fseek(fin, 0, SEEK_END);
  *bufferSize = ftell(fin);
  fseek(fin, 0, SEEK_SET);

  if (*bufferSize == 0)
    return NULL;
  
  fprintf(stderr, "%d char in file\n", *bufferSize);

  /* put the binary file in a buffer */
  buffer = (char*) malloc(*bufferSize * sizeof(char));
  memset(buffer, 0, *bufferSize);
  fread(buffer, 1, *bufferSize, fin);
  fclose(fin);
  
  return buffer;
}

static
void transposebmp(const char* filename)
{
  int i = 0, bufferSize, j;

  /* iBuffer = input buffer */
  char* iBuffer = file2buffer(filename, &bufferSize);
  
  if (iBuffer == NULL)
    {
      fprintf(stderr, "Null file size\n");
      fflush(stderr);
      exit(-1);
    }
  
  /* open file for writing it */
  const char* out_filename = "/tmp/transposed.bmp";
  FILE* fout = fopen(out_filename, "w");
  fprintf(stderr, "output filename : %s\n", out_filename);

  size_t bmpheadersize = bufferSize - (bmpwidth * bmpheight);
  /* We fwrite the bmp header */
  if (fwrite(iBuffer, 1, bmpheadersize, fout) != bmpheadersize)
    {
      fprintf(stderr, "error: header fwrite failed\n");
      fclose(fout);
      return;
    }

  /* it's done, close it */
  fclose(fout);
}
