#include <stdio.h>

typedef struct
{
  int width;
  int height;
  int* data;
} myStruct;

void print_struct(myStruct st)
{
  printf("myStruct: width(%d), height(%d), *data(%p), data(%d)\n", st.width, st.height, st.data, *st.data);
}

int main()
{
  myStruct A;
  A.width = 400;
  A.height = 500;
  int x = 12;
  A.data = &x;

  print_struct(A);

  myStruct B;
  B.width = 100;
  B.height = 100;
  int y = 17;
  B.data = &y;
  
  print_struct(B);
  
  B = A;
  print_struct(B);
  
  return 0;
}
