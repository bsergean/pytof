#include <stdio.h>

#define PRINT_SIZEOF(type) printf("sizeof(%s) = %d\n", #type, sizeof(#type))

int main()
{
  printf("sizeof(char) = %d\n", sizeof(char));
  printf("sizeof(unsigned char) = %d\n", sizeof(unsigned char));
  printf("sizeof(short) = %d\n", sizeof(short));
  printf("sizeof(unsigned short) = %d\n", sizeof(unsigned short));
  printf("sizeof(int) = %d\n", sizeof(int));
  printf("sizeof(unsigned int) = %d\n", sizeof(unsigned int));
  printf("sizeof(long) = %d\n", sizeof(long));
  printf("sizeof(unsigned long) = %d\n", sizeof(unsigned long));
  printf("sizeof(long long) = %d\n", sizeof(long long));
  printf("sizeof(unsigned long long) = %d\n", sizeof(unsigned long long));
  printf("sizeof(float) = %d\n", sizeof(float));
  printf("sizeof(double) = %d\n", sizeof(double));

  long l = 100000000000;
  printf("long l = %ld\n", l);

  //long superlong 223372036854775807L; Too long for Linux
  //printf("long superlong = %ld\n", superlong);
  
  return 0;
}
