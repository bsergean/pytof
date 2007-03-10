#include <stdio.h>

int main()
{
  int tab[10];
  int i = 3;
  tab[i] = 12;
  printf("tab[i] = %d\n", tab[i]);
  printf("i[tab] = %d\n", i[tab]);
}
