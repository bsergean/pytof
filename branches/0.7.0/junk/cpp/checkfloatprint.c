#include <stdio.h>

#define FALSE 0
#define TRUE 1

int print_float(float a)
{
  char strfloat[512];
  int float_size = sprintf(strfloat, "%f", a);

  printf("strlen(\"%f\") : %d\n", a, float_size);
 		  
  if (float_size != printf("%s", strfloat))
    {
      return FALSE;
    }
  return TRUE;
}


int main()
{
  float f = 1534.567;
  if (print_float(f))
    puts("\nOK");
  else
    puts("\nProblem");
}
