#include <stdio.h>

class CameraInfos
{
public:
  CameraInfos(int _a, int _b);
  CameraInfos() {}

  void one() { puts("one"); }
  void two() { puts("two"); }
  void three() { puts("three"); }
};

typedef void (CameraInfos::*myCameraInfosMenberFn)(void);

myCameraInfosMenberFn array[] = 
  {
    &CameraInfos::one,
    &CameraInfos::two,
    &CameraInfos::three
  };

int main()
{
  printf("size of array : %d", sizeof(array) / sizeof(myCameraInfosMenberFn) );
  
  return 0;
}
