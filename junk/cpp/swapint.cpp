#include <stdio.h>
#include <malloc.h>

int swapint(int w)
{
  return ((w << 24) | ((w & 0x0000ff00UL) << 8) | ((w & 0x00ff0000UL) >> 8) | ((w & 0xff000000UL) >> 24));
}

int test1()
{
  unsigned int i = 12;

  printf("12 = %d\n", swapint(i));
}

int main()
{
  test1();
}
