#include <stdio.h>
#include "string.h"

unsigned char hexa2int(unsigne char A, unsigne char B)
{
  switch (A)
}
// convert a hex color string to three integer RGB values.
// returns zero on success, non-zero on error.
int
hex2rgb(const char * hex, int& red, int& green, int& blue)
{
    unsigned long val;

    if (NULL == hex)
    {
        red = green = blue = 0;
        return 1;
    }

    // convert the hex string to an unsigned long int.
    // val will be zero if 'hex' is invalid.
    // Note: we should check 'errno' after this call
    //       to see if a conversion error occurred;
    //       see the docs for strtoul().
    val = strtoul(hex, NULL, 16);
    red = ((val & 0xff0000) >> 16);
    green = ((val & 0xff00) >> 8);
    blue = (val & 0xff);

    return 0;

} 

int main()
{
  char string_to_parse [] = "FFFFFF";

  unsigned char r1, r2, g1, g2, b1, b2;
  sscanf(string_to_parse,
	 "%c%c%c%c%c%c",
	 &r1, &r2, &g1, &g2, &b1, &b2);

  printf("%c%c%c%c%c%c\n", r1, r2, g1, g2, b1, b2);
  
  return 0;
}
