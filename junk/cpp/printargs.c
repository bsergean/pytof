#include <stdio.h>

int main(int argc, char** argv)
{
  printf("#arguments : %d\n", argc-1);
  while (argc--)
    {
      if (argc == 0)
	printf("cmd name : ");
      else
	printf("argument %d : ", argc);
	  
      puts(argv[argc]);
    }
}
