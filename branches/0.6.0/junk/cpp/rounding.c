#include <stdio.h>
#include <math.h>

#define mynearbyint(f) floor(f + 0.5)

int main()
{
  // rounding  
  printf("ceil\n");
  printf("%d\n", (int) ceil(4.99f) );
  printf("%d\n", (int) ceil(5.01f) );
  printf("%d\n", (int) ceil(-5.01f) );
  printf("%d\n", (int) ceil(-4.99f) );

  printf("floor\n");
  printf("%d\n", (int) floor(4.99f) );
  printf("%d\n", (int) floor(5.01f) );
  printf("%d\n", (int) floor(-5.01f) );
  printf("%d\n", (int) floor(-4.99f) );

  printf("int cast\n");
  printf("%d\n", (int) 4.99f );
  printf("%d\n", (int) 5.01f );
  printf("%d\n", (int) -5.01f );
  printf("%d\n", (int) -4.99f );

#ifndef sun
  printf("nearbyint\n");
  printf("%d\n", (int) nearbyint(4.99f) );
  printf("%d\n", (int) nearbyint(5.01f) );
  printf("%d\n", (int) nearbyint(-5.01f) );
  printf("%d\n", (int) nearbyint(-4.99f) );

  printf("round\n");
  printf("%d\n", (int) round(4.99f) );
  printf("%d\n", (int) round(5.01f) );
  printf("%d\n", (int) round(-5.01f) );
  printf("%d\n", (int) round(-4.99f) );
#endif
  
  printf("mynearbyint\n");
  printf("%d\n", (int) mynearbyint(4.99f) );
  printf("%d\n", (int) mynearbyint(5.01f) );
  printf("%d\n", (int) mynearbyint(-5.01f) );
  printf("%d\n", (int) mynearbyint(-4.99f) );
  
  return 0;
}
