/*

 Wants to mimic python zfill function at printf time

 |  zfill(...)
 |      S.zfill(width) -> string
 |
 |      Pad a numeric string S with zeros on the left, to fill a field
 |      of the specified width.  The string S is never truncated.

*/

#include <stdio.h>

int main()
{
  int a = 7;
  printf("07 = %02d\n",a);
  printf("007 = %03d\n",a);
}
